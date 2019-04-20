"""
Peacock Exchange Module

Handles order requests from the Brokers, matches orders in OrderBooks, returns
order updates and market snapshots to subscribers (Brokers and MarketData).
"""

import datetime
import threading
import time
import math
import xml.etree.ElementTree as ElementTree
from pathlib import Path
import os

from concurrent import futures
from collections import deque, namedtuple, defaultdict

import grpc

from ..common import Limits, ValueWithSpeed
from ..common.recipes import BatchMessenger
from ..common import serialize

from .._pyprotos import exchange_pb2 as pb2, exchange_pb2_grpc as pb2_grpc
from .._pyprotos import common_pb2
from .._pyprotos.common_pb2 import (
    OK, BID, ASK, Empty, RpcResponse,
    NEW_ORDER, CANCEL_ORDER,
    SERVICE_UNAVAILABLE, INVALID_BROKER_ID, INVALID_ORDER_ID,
    INVALID_VOLUME, INVALID_PRICE, INVALID_SYMBOL, INVALID_SIDE,
    ORDER_ACCEPTED, ORDER_TRADED, ORDER_FINISHED, ORDER_CANCELLED,
    ORDER_REJECTED,
    INVALID_REQUEST, UNKNOWN_ERROR
)

from .clock import Clock
from .orderbook import OrderBook


################################################################################
# Exchange, the Main Process and gRPC Servicer
################################################################################

_InstrumentInfo = namedtuple('_InstrumentInfo', [
    'id', 'symbol', 'name', 'init_price', 'tick'
])

# Hack to circumvent gRPC's TypeError in MergeFrom on MacOS
TradeRecordType = type(pb2.MarketUpdate().instruments.add().trades.add())
QuoteRecordType = type(pb2.MarketUpdate().instruments.add().bid_quotes.add())

_OrderTraded = namedtuple('_OrderTraded', [
    'symbol', 'timestamp', 'traded_price', 'traded_volume',
    'bid_broker_id', 'bid_trader_id', 'bid_order_id',
    'ask_broker_id', 'ask_trader_id', 'ask_order_id'
])


class Exchange(pb2_grpc.ExchangeServicer):
    """Peacock Exchange Service

    Implements an API for handling order-related requests from Broker, or
    allowing Broker/MarketData to subscribe for asynchronous responses of
    order updates and market snapshots.
    """

    class Config:
        """Configuration for Exchange."""

        def __init__(self, filename):
            import os.path as path
            full_path = path.join(path.dirname(__file__), filename)
            root = ElementTree.parse(full_path).getroot()
            self._log_price = (root.get('log_price', 'true') == "true")
            self.deliver_interval_second = int(root.get('deliver_interval_second', 900))
            self.twap_range = int(root.get('twap_range', 60))
            self.maker_bp_diff = float(root.get('maker_bp_diff', 0.1))
            self.trader_num = int(root.get('trader_num', 20))

            self.instruments = {
                node.get('symbol'): _InstrumentInfo(
                    id=id, symbol=node.get('symbol'), name=node.get('name'),
                    init_price=float(node.get('init_price')),
                    tick=float(node.get('tick'))
                )
                for id, node in enumerate(
                    root.find('instruments').findall('instrument')
                )
            }
            assert self.instruments, 'No instrument'

            self.market_interval = 0.0001  # 100 updates/sec

        @property
        def log_price(self):
            return self._log_price

    def __init__(self, port, config_filename='config.xml'):
        self._config = Exchange.Config(config_filename)
        self.robot_broker_id = 101
        self.trader_num = self._config.trader_num
        self.maker_bp_diff = self._config.maker_bp_diff
        base = str(Path(__file__).resolve().parents[2])
        filename = "exchange_history.{}.log".format(time.strftime("%Y%m%d_%H%M"))
        filename = os.path.join(base, filename)
        self._log_file = open(filename, 'w')

        self._is_started = False
        self._clock = Clock()

        # Statistics
        self._statistics = _Statistics()

        # gRPC server
        self._server = None
        self._port = port

        self._history_snapshot_list = []
        self._history_snapshot_size_threshold = 50000
        self._history_snapshot_dump_file_name = 'dump/tradelog_@time.json'
        self._serialize = serialize.JsonSerializer(compress=True)  # compress the history file

        self._orderbooks = {
            symbol: OrderBook(ins.init_price, ins.tick, symbol if self._config.log_price else None)
            for symbol, ins in self._config.instruments.items()
        }
        self._prices = {
            symbol: ins.init_price
            for symbol, ins in self._config.instruments.items()
        }

        # Ensures processing results in each order book is order-preserving.
        self._orderbook_locks = {
            symbol: threading.Lock()
            for symbol in self._config.instruments.keys()
        }

        # Each Broker has a queue here, indexed by Broker ID, to temporarily store trade records not yet fetched.
        self._broker_messengers = defaultdict(BatchMessenger)

        # A queue to store market updates for the MarketData to fetch.
        self._market_queue = deque([
            _InstrumentUpdate(
                symbol=symbol, trades=[TradeRecordType(
                    timestamp=0, price=ins.init_price, volume=0
                )], bid_quotes={}, ask_quotes={}
            )
            for symbol, ins in self._config.instruments.items()
        ])

        # histogram of lags in milliseconds
        self._t2t_pre_lags = defaultdict(int)
        self._t2t_post_lags = defaultdict(int)

        self.last_deliver_time = 0
        self.broker_last_deliver_time = dict()
        self.deliver_pnl = dict()
        self.symbol_last_price = dict()
        self.symbol_history_price = defaultdict(deque)
        self.symbol_twap_price = dict()
        self.symbol_sum_twap_price = defaultdict(float)
        self.twap_range = self._config.twap_range
        self.work_lock = threading.Lock()
        self.deliver_lock = threading.Lock()
        self.underlying_map = {
            'A001.PSE': 'A000.PSE', 'A002.PSE': 'A000.PSE',
            'B001.PSE': 'B000.PSE', 'B002.PSE': 'B000.PSE',
        }
        self.next_clock_ts = 1
        # key1: trader_id, key2: symbol or 'all',
        # value: a list, [check times, did times, percent]
        self.market_make_records = defaultdict(dict)
        self.thread = threading.Thread(target=self.work)
        self.thread.start()

    def work(self):
        if self._config.deliver_interval_second == 0:
            return
        while True:
            ts = int(self._clock.timestamp)
            if ts < self.next_clock_ts:
                time.sleep(0.2)
                continue
            self.next_clock_ts += 1
            # start to check deliver price when deliver within one minute
            next_deliver_ts_zone = self.last_deliver_time + self._config.deliver_interval_second - 60
            is_in_deliver_zone = ts > next_deliver_ts_zone
            # compute deliver price
            with self.work_lock:
                tmp_last_price = self.symbol_last_price.copy()
            for symbol, record in tmp_last_price.items():
                if not is_in_deliver_zone:
                    self.symbol_twap_price[symbol] = record.price
                    continue
                if len(self.symbol_history_price[symbol]) >= self.twap_range:
                    removed = self.symbol_history_price[symbol].popleft()
                    self.symbol_sum_twap_price[symbol] -= removed
                self.symbol_history_price[symbol].append(record.price)
                self.symbol_sum_twap_price[symbol] += record.price
                self.symbol_twap_price[symbol] = self.symbol_sum_twap_price[symbol] / \
                    len(self.symbol_history_price[symbol])

            for symbol, order_book in self._orderbooks.items():
                price_diff = 0.2
                trader_orderbook_buy = defaultdict(dict)
                trader_orderbook_sell = defaultdict(dict)
                with self._orderbook_locks[symbol]:
                    for int_id, order_node in order_book.bids.order_nodes.items():
                        order = order_node.order
                        if order.broker_id == self.robot_broker_id or order.volume == 0:
                            continue
                        if order.trader_id not in trader_orderbook_buy or \
                           round(order.price, 2) not in trader_orderbook_buy[order.trader_id]:
                            trader_orderbook_buy[order.trader_id][round(order.price, 2)] = order.volume
                        else:
                            trader_orderbook_buy[order.trader_id][round(order.price, 2)] += order.volume
                    for int_id, order_node in order_book.asks.order_nodes.items():
                        order = order_node.order
                        if order.broker_id == self.robot_broker_id or order.volume == 0:
                            continue
                        if order.trader_id not in trader_orderbook_sell or \
                           round(order.price, 2) not in trader_orderbook_sell[order.trader_id]:
                            trader_orderbook_sell[order.trader_id][round(order.price, 2)] = order.volume
                        else:
                            trader_orderbook_sell[order.trader_id][round(order.price, 2)] += order.volume
                for i in range(self.trader_num):
                    if i not in trader_orderbook_buy:
                        self.update_market_make_record(symbol, i, False)
                    elif i not in trader_orderbook_sell:
                        self.update_market_make_record(symbol, i, False)
                    else:
                        valid_best_buy = 0.0
                        valid_best_sell = 9999.0
                        buy_volume = 0
                        sell_volume = 0
                        for price, volume in sorted(trader_orderbook_buy[i].items(), key=lambda t: t[0], reverse=True):
                            #print(i, symbol, 'buy', price, volume)
                            buy_volume += volume
                            if buy_volume >= 10:
                                valid_best_buy = price
                                break
                        for price, volume in sorted(trader_orderbook_sell[i].items(), key=lambda t: t[0]):
                            #print(i, symbol, 'sell', price, volume)
                            sell_volume += volume
                            if sell_volume >= 10:
                                valid_best_sell = price
                                break
                        #print(i, symbol, 'valid best buy', valid_best_buy, 'valid best sell', valid_best_sell)
                        if valid_best_sell - valid_best_buy > price_diff:
                            self.update_market_make_record(symbol, i, False)
                        else:
                            self.update_market_make_record(symbol, i, True)

            # check if need to deliver
            deliver_ts = int(self.next_clock_ts / self._config.deliver_interval_second)
            deliver_ts *= self._config.deliver_interval_second
            if deliver_ts <= self.last_deliver_time:
                continue
            # if need deliver
            self.last_deliver_time = deliver_ts
            with self.deliver_lock:
                for symbol, underlying in self.underlying_map.items():
                    dp = self.get_deliver_price(symbol)
                    order_book = self._orderbooks[symbol]
                    mp = round((order_book.bids.max_price + order_book.asks.min_price) / 2, 2)
                    print('Deliver', symbol, 'dp', dp, 'mp', mp)
                    self.deliver_pnl[symbol] = dp - mp
            for symbol in self.symbol_twap_price.keys():
                self.symbol_history_price[symbol].clear()
                self.symbol_sum_twap_price[symbol] = 0

    def update_market_make_record(self, symbol, trader_id, is_complete):
        if '000' in symbol:
            return
        if 'all' not in self.market_make_records[trader_id]:
            self.market_make_records[trader_id]['all'] = [0, 0, 0]
        if symbol not in self.market_make_records[trader_id]:
            self.market_make_records[trader_id][symbol] = [0, 0, 0]
        self.market_make_records[trader_id][symbol][1] += 1
        self.market_make_records[trader_id]['all'][1] += 1
        if is_complete:
            self.market_make_records[trader_id][symbol][0] += 1
            self.market_make_records[trader_id]['all'][0] += 1
        self.market_make_records[trader_id][symbol][2] = \
            self.market_make_records[trader_id][symbol][0] / self.market_make_records[trader_id][symbol][1]
        self.market_make_records[trader_id]['all'][2] = \
            self.market_make_records[trader_id]['all'][0] / self.market_make_records[trader_id]['all'][1]

    def get_market_make_price_diff(self, last_price_dict, symbol):
        if symbol not in last_price_dict:
            return 0
        current_price = last_price_dict[symbol].price
        diff = current_price * self.maker_bp_diff
        return diff

    def start(self):
        """Starts the Exchange module."""
        if self._is_started:
            raise NotImplementedError('Re-starting is not supported yet')

        self._server = grpc.server(futures.ThreadPoolExecutor())
        pb2_grpc.add_ExchangeServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

        self._is_started = True

    def get_deliver_price(self, symbol):
        if symbol not in self.underlying_map:
            return 0
        if self.underlying_map[symbol] in self.symbol_twap_price:
            price = self.symbol_twap_price[self.underlying_map[symbol]]
            if symbol == 'A001.PSE' or symbol == 'B001.PSE':
                return price
            elif symbol == 'A002.PSE':
                return price * price / 100
            elif symbol == 'B002.PSE':
                if price > 0:
                    return 10 * math.sqrt(price)
                else:
                    return price
            return price
        if symbol in self.symbol_twap_price:
            return self.symbol_twap_price[symbol]
        if symbol in self.symbol_last_price:
            return self.symbol_last_price[symbol].price
        return 0

    def stop(self):
        """Stops the Exchange module."""
        if not self._is_started:
            raise NotImplementedError('Exchange is not started')

        # Stops accepting new requests
        self._is_started = False

        for symbol, order_book in self._orderbooks.items():
            with self._orderbook_locks[symbol]:
                order_book.close()

        if self._server:
            self._server.stop(0).wait()
            del self._server
            self._server = None

    def list_instruments(self, request, _=None):
        """(API) Returns basic info of the instruments in the exchange."""
        response = common_pb2.InstrumentInfoList()
        response.instruments.extend([
            common_pb2.InstrumentInfo(
                symbol=symbol, init_price=inst.init_price, tick=inst.tick,
                last_price=self._prices[symbol]
            ) for symbol, inst in self._config.instruments.items()
        ])
        return response

    def new_order(self, request: pb2.BrokerRequest, _=None):
        """(API) Adds a new order to the Exchange."""
        # T2T lag test
        if request.orig_timestamp > 3:
            lag = self._clock.timestamp - request.orig_timestamp
            self._t2t_pre_lags[int(100 * lag)] += 1

        # with self._statistics.lock:
        self._statistics.api_call_count.value += 1

        # Check for request errors:
        result_code = OK

        if not self._is_started:
            result_code = SERVICE_UNAVAILABLE
        elif request.request_type != NEW_ORDER:
            result_code = INVALID_REQUEST
        elif request.broker_id <= 0:
            result_code = INVALID_BROKER_ID
        elif request.order_id <= 0:
            result_code = INVALID_ORDER_ID
        elif request.symbol not in self._config.instruments:
            result_code = INVALID_SYMBOL
        elif not (request.side == BID or request.side == ASK):
            result_code = INVALID_SIDE
        elif not request.is_market and request.price < Limits.MIN_PRICE:
            result_code = INVALID_PRICE
        elif request.broker_id != self.robot_broker_id and not Limits.is_volume_valid(request.volume):
            result_code = INVALID_VOLUME

        # Push an initial order event to the Broker
        order_state = ORDER_ACCEPTED if result_code == OK else ORDER_REJECTED

        messenger = self._broker_messengers[request.broker_id]
        messenger.push(_BrokerUpdate(
            symbol=None, last_price=None,   # no price is updated (yet)
            order_events=[pb2.OrderEvent(
                state=order_state,
                trader_id=request.trader_id,
                order_id=request.order_id
            )]
        ))

        if result_code == OK:
            # Lock to ensure sequential order matching
            with self._orderbook_locks[request.symbol]:
                # Process the new order
                orderbook = self._orderbooks[request.symbol]

                trades, quotes, left_cancelled = orderbook.new_order(
                    request.broker_id, request.trader_id, request.order_id,
                    request.side, None if request.is_market else request.price,
                    request.volume
                )

                if self._log_file is not None:
                    if request.broker_id != self.robot_broker_id:
                        self._log_file.write('New Order bi={} ti={} oi={} symbol={} s={} pos_type={} p={} v={} ts={}\n'.format(
                            request.broker_id, request.trader_id, request.order_id, request.symbol, request.side,
                            request.pos_type, None if request.is_market else request.price, request.volume,
                            datetime.datetime.now().strftime("%H:%M:%S")
                        ))
                    for trade in trades:
                        if trade.bid_broker_id != self.robot_broker_id or trade.ask_broker_id != self.robot_broker_id:
                            self._log_file.write('Trade p={} v={} bbi={} bti={} boi={} bor={} '.format(
                                trade.price, trade.volume, trade.bid_broker_id, trade.bid_trader_id,
                                trade.bid_order_id, trade.bid_order_remains
                            ))
                            self._log_file.write('abi={} ati={} aoi={} aor={} ts={}\n'.format(
                                trade.ask_broker_id, trade.ask_trader_id, trade.ask_order_id, trade.ask_order_remains,
                                datetime.datetime.now().strftime("%H:%M:%S")
                            ))
                    self._log_file.flush()

                # Trade records are to be dispatched to relevant Broker queues.
                # Both trade records and quote updates are dispatched to the
                # market queue.
                self._dispatch_results(request, trades, quotes)

                if left_cancelled:
                    assert request.is_market

                    # Push an ORDER_CANCELLED event to the Broker
                    messenger = self._broker_messengers[request.broker_id]
                    messenger.push(_BrokerUpdate(
                        symbol=None, last_price=None,
                        order_events=[pb2.OrderEvent(
                            state=ORDER_CANCELLED,
                            trader_id=request.trader_id,
                            order_id=request.order_id
                        )]
                    ))

            # with self._statistics.lock:
            self._statistics.new_order_count.value += 1

        if request.orig_timestamp > 3:
            lag = self._clock.timestamp - request.orig_timestamp
            self._t2t_post_lags[int(100 * lag)] += 1

        # Order events and updated prices will be collected.
        return self._get_response_for(request, result_code)

    def cancel_order(self, request: pb2.BrokerRequest, _=None):
        """(API) Cancels an existing order in the Exchange."""
        # with self._statistics.lock:
        self._statistics.api_call_count.value += 1

        # Check for request errors:
        result_code = OK

        if not self._is_started:
            result_code = SERVICE_UNAVAILABLE
        if request.request_type != CANCEL_ORDER:
            result_code = INVALID_REQUEST
        if request.broker_id <= 0:
            result_code = INVALID_BROKER_ID
        if request.order_id <= 0:
            result_code = INVALID_ORDER_ID
        if request.symbol not in self._config.instruments:
            result_code = INVALID_SYMBOL

        if result_code == OK:
            # Lock to ensure sequential order processing
            with self._orderbook_locks[request.symbol]:
                # (Try to) remove the order from the book
                orderbook = self._orderbooks[request.symbol]
                quote = orderbook.remove_order(request.broker_id, request.order_id)

                if quote is None:
                    # Order does not exist in the book
                    return self._get_response_for(request, INVALID_ORDER_ID)

                if self._log_file is not None and request.broker_id != self.robot_broker_id:
                    self._log_file.write('Cancelled bi={} oi={} ti={} ts={}\n'.format(
                        request.broker_id, request.order_id, request.trader_id, datetime.datetime.now().strftime("%H:%M:%S")))
                    self._log_file.flush()

                # Push an ORDER_CANCELLED event to the Broker
                messenger = self._broker_messengers[request.broker_id]
                messenger.push(_BrokerUpdate(
                    symbol=None, last_price=None,   # no price is updated (yet)
                    order_events=[pb2.OrderEvent(
                        state=ORDER_CANCELLED,
                        trader_id=request.trader_id,
                        order_id=request.order_id
                    )]
                ))

                self._dispatch_results(request, None, [quote])

            # with self._statistics.lock:
            self._statistics.cancel_order_count.value += 1

        return self._get_response_for(request)

    def fetch_updates(self, request, _=None):
        """(API) TODO: refactor"""
        assert request.request_type == common_pb2.INCREMENTAL_INFO

        return self._get_response_for(request)

    def fetch_deliver_price(self, request, _=None):
        response = pb2.DeliverResponse(
            timestamp=self._clock.timestamp
        )
        broker_id = request.broker_id
        if self.last_deliver_time == 0:
            return response
        if broker_id in self.broker_last_deliver_time \
                and self.broker_last_deliver_time[broker_id] >= self.last_deliver_time:
            return response
        self.broker_last_deliver_time[broker_id] = self.last_deliver_time
        response.deliveries.extend([
            pb2.InstrumentPrice(symbol=symbol, price=price)
            for symbol, price in self.deliver_pnl.items()
        ])
        return response

    def subscribe_market(self, request: Empty, _=None):
        """(API) Obtains a response stream with updating market snapshots."""
        # Subscription ends anyway when Exchange stops
        while self._is_started:
            if not self._market_queue:
                time.sleep(0.01)
                continue

            instruments = {}

            # Get everything on the queue to create a response
            while self._market_queue:
                update = self._market_queue.popleft()  # _InstrumentUpdate

                if update.symbol in instruments:
                    dst = instruments[update.symbol]
                    dst.trades.extend(update.trades)
                    dst.bid_quotes.update(update.bid_quotes)
                    dst.ask_quotes.update(update.ask_quotes)
                else:
                    instruments[update.symbol] = update

            response = pb2.MarketUpdate(timestamp=self._clock.timestamp)
            for src_inst in instruments.values():
                dst_inst = response.instruments.add()

                dst_inst.symbol = src_inst.symbol
                dst_inst.trades.extend(src_inst.trades)
                dst_inst.bid_quotes.extend(src_inst.bid_quotes.values())
                dst_inst.ask_quotes.extend(src_inst.ask_quotes.values())
                dst_inst.deliver_price = self.get_deliver_price(src_inst.symbol)

            yield response

            # with self._statistics.lock:
            self._statistics.market_update_count.value += 1

    def status(self, request: Empty, _=None):
        """(API) Returns the status of this Exchange."""
        # with self._statistics.lock:
        self._statistics.update_speed()

        # Calculate average t2t delay
        total_delay = 0
        total_count = 0
        for i, n in self._t2t_pre_lags.items():
            total_delay += i * 10 * n
            total_count += n
        avg_t2t = total_delay / total_count if total_count > 0 else 0

        return pb2.ExchangeStatus(
            timestamp=self._clock.timestamp,
            api_call_speed=self._statistics.api_call_count.speed,
            new_order_speed=self._statistics.new_order_count.speed,
            cancel_order_speed=self._statistics.cancel_order_count.speed,
            market_update_speed=self._statistics.market_update_count.speed,
            average_t2t=avg_t2t,
            broker_count=len(self._broker_messengers)
        )

    def print_status(self):
        """Debugging output."""
        stats = self._statistics
        stats.update_speed()
        print('[EXCHANGE] %s RPC: %.1f/s  NEW: %.1f/s  CANCEL: %.1f/s  UPD: %.1f/s' % (
            str(self._clock), stats.api_call_count.speed,
            stats.new_order_count.speed, stats.cancel_order_count.speed,
            stats.market_update_count.speed
        ))

    def __del__(self):
        print('[Exchange] dump tradelog before leave.')
        if self._history_snapshot_list:
            fn = self._history_snapshot_dump_file_name.replace(
                '@time', time.strftime('%Z_%Y%m%d_%H-%M-%S', time.localtime()))
            self._serialize.to_file(self._history_snapshot_list, fn, no_blocking=True)
            del self._history_snapshot_list[:]

    def _save_snapshot_to_history(self, snapshot: _OrderTraded):
        self._history_snapshot_list.append(snapshot)
        if len(self._history_snapshot_list) >= self._history_snapshot_size_threshold:
            fn = self._history_snapshot_dump_file_name.replace(
                '@time', time.strftime('%Z_%Y%m%d_%H-%M-%S', time.localtime()))
            self._serialize.to_file(self._history_snapshot_list, fn, no_blocking=True)
            del self._history_snapshot_list[:]

    def _dispatch_results(self, request, trades, quotes):
        """Pushes a list of order updates and orderbook updates to the
        relevant recipients' queues.

        Data pushed to Broker queues are of type _BrokerUpdate.
        Data pushed to MarketData queue are of type _MarketUpdate.

        Args:
            trades: a list of orderbook.TradeRecord
            quotes: a list of orderbook.QuoteRecord
        """
        if trades:
            broker_events = defaultdict(list)  # broker_id -> [pb2.OrderEvent]
            # Split trade records into two sides and regroup by brokers
            for trade in trades:
                broker_events[trade.bid_broker_id].append(pb2.OrderEvent(
                    state=ORDER_TRADED if trade.bid_order_remains else ORDER_FINISHED,
                    trader_id=trade.bid_trader_id,
                    order_id=trade.bid_order_id,
                    price=trade.price,
                    volume=trade.volume,
                    left_volume=trade.bid_order_remains
                ))

                broker_events[trade.ask_broker_id].append(pb2.OrderEvent(
                    state=ORDER_TRADED if trade.ask_order_remains else ORDER_FINISHED,
                    trader_id=trade.ask_trader_id,
                    order_id=trade.ask_order_id,
                    price=trade.price,
                    volume=trade.volume,
                    left_volume=trade.ask_order_remains
                ))
                log = _OrderTraded(
                    symbol=request.symbol,
                    timestamp=self._clock.timestamp,
                    traded_price=trade.price,
                    traded_volume=trade.volume,
                    bid_broker_id=trade.bid_broker_id,
                    bid_trader_id=trade.bid_trader_id,
                    bid_order_id=trade.bid_order_id,
                    ask_broker_id=trade.ask_broker_id,
                    ask_trader_id=trade.ask_trader_id,
                    ask_order_id=trade.ask_order_id,
                )
                self._save_snapshot_to_history(log)

            for broker_id, messenger in self._broker_messengers.items():
                # Assemble an update to be queued for the Broker
                # Note: all Brokers can get updated price
                messenger.push(_BrokerUpdate(
                    symbol=request.symbol, last_price=trades[-1].price,
                    order_events=broker_events[broker_id]
                ))

        # Push simplified trade and quote records to the MarketData
        timestamp = self._clock.timestamp
        trade_records = [
            TradeRecordType(
                timestamp=timestamp, price=trade.price, volume=trade.volume
            )
            for trade in trades or []
        ]
        with self.work_lock:
            for record in trade_records:
                self.symbol_last_price[request.symbol] = record
        self._market_queue.append(_InstrumentUpdate(
            symbol=request.symbol,
            trades=trade_records,
            bid_quotes={
                quote.price: QuoteRecordType(
                    price=quote.price, volume=quote.volume,
                    order_count=quote.order_count
                )
                for quote in quotes if quote.side == BID
            },
            ask_quotes={
                quote.price: QuoteRecordType(
                    price=quote.price, volume=quote.volume,
                    order_count=quote.order_count
                )
                for quote in quotes if quote.side == ASK
            }
        ))

    def _get_response_for(self, request: pb2.BrokerRequest, result_code=OK):
        """Returns a BrokerResponse for a given Broker.

        Contains trade records and/or instrument prices that should be
        fetched by the Broker.
        """
        response = pb2.BrokerResponse(
            timestamp=self._clock.timestamp, result_code=result_code
        )

        # Fetch any queued trade records or price updates
        messenger = self._broker_messengers[request.broker_id]

        response.batch_id = messenger.start_batch()

        sym_prices = {}  # Tracks prices affected by the updates
        while not messenger.is_empty:
            msg = messenger.pop()  # _BrokerUpdate

            if msg.symbol and msg.last_price:
                sym_prices[msg.symbol] = msg.last_price
            if msg.order_events:
                response.order_events.extend(msg.order_events)
                # if request.broker_id == 2:
                #     for order_event in msg.order_events:
                #         print(request.broker_id, order_event.trader_id, order_event.order_id, order_event.state, order_event.price, order_event.volume, order_event.left_volume)

        response.prices.extend([
            pb2.InstrumentPrice(symbol=symbol, price=price)
            for symbol, price in sym_prices.items()
        ])

        if request.broker_id != self.robot_broker_id:
            for trader_id, results in self.market_make_records.items():
                info = response.traders.add()
                info.trader_id = trader_id
                for symbol, record in self.market_make_records[trader_id].items():
                    mrecord = info.market_records.add()
                    mrecord.symbol = symbol
                    mrecord.complete = record[0]
                    mrecord.total = record[1]
                    mrecord.percent = record[2]

        messenger.end_batch()

        return response


################################################################################
# Data types internal to the Exchange
################################################################################

class _Statistics:
    """Runtime statistics of the Exchange."""

    def __init__(self):
        self.api_call_count = ValueWithSpeed()
        self.new_order_count = ValueWithSpeed()
        self.cancel_order_count = ValueWithSpeed()
        self.market_update_count = ValueWithSpeed()

        self.traded_money = ValueWithSpeed()
        self.traded_volume = ValueWithSpeed()

        self.lock = threading.Lock()

        self._last_timestamp = datetime.datetime.utcnow().timestamp()
        self._min_interval = 0.5    # seconds

    @property
    def order_request_count(self):
        """Total number of requests received."""
        return self.new_order_count.value + self.cancel_order_count.value

    @property
    def order_request_speed(self):
        """Current speed of incoming requests."""
        return self.new_order_count.speed + self.cancel_order_count.speed

    def update_speed(self):
        """Recalculates the speed of counters."""
        elapsed = datetime.datetime.utcnow().timestamp() - self._last_timestamp
        if elapsed <= self._min_interval:
            return

        self._last_timestamp += elapsed

        self.api_call_count.update_speed(elapsed)
        self.new_order_count.update_speed(elapsed)
        self.cancel_order_count.update_speed(elapsed)
        self.market_update_count.update_speed(elapsed)
        self.traded_money.update_speed(elapsed)
        self.traded_volume.update_speed(elapsed)


# "Take-away" message for a Broker
# Attributes:
#     symbol: indicates the instrument this update is about.
#     last_price: latest trade price of the instrument.
#     order_events: a list of exchange_pb2.OrderEvent.
_BrokerUpdate = namedtuple('_BrokerUpdate', [
    'symbol', 'last_price', 'order_events'
])


# "Take-away" message for the MarketData
# Attributes:
#     symbol: indicates the instrument this update is about.
#     trades: a list of common_pb2.TradeRecord.
#     bid_quotes: a price-indexed dict of common_pb2.QuoteRecord.
#     ask_quotes: a price-indexed dict of common_pb2.QuoteRecord.
_InstrumentUpdate = namedtuple('_InstrumentUpdate', [
    'symbol', 'trades', 'bid_quotes', 'ask_quotes'
])
