"""
Peacock Market Data module
"""

from concurrent import futures
from collections import deque

import time
import threading
import grpc

from ..common import serialize
from ..common.pob import PseudoOrderBook
from .._pyprotos import market_data_pb2 as pb2, market_data_pb2_grpc as pb2_grpc
from .._pyprotos import common_pb2, exchange_pb2
from .._pyprotos.common_pb2 import (
    Empty, BID, ASK
)
from .._pyprotos.exchange_pb2_grpc import ExchangeStub


# Hack to circumvent gRPC's TypeError in MergeFrom on MacOS
TradeRecordType = type(pb2.MarketSnapshot().instruments.add().last_trades.add())
QuoteRecordType = type(pb2.MarketSnapshot().instruments.add().bid_levels.add())


class _InstrumentData:
    """Static and dynamic data of an instrument."""

    def __init__(self, info: common_pb2.InstrumentInfo, snapshot_interval):
        self.symbol = info.symbol
        self.name = info.name
        self.init_price = info.init_price
        self.tick = info.tick
        self.pob = PseudoOrderBook(info.symbol, info.init_price)
        self.snapshots = deque(maxlen=2000)
        # self.minute_ohlc = deque(maxlen=2000)
        self._snapshot_interval = snapshot_interval
        self._last_snapshot_time = 0

        self._history_snapshot_interval = 0.2  # dump file
        self._history_snapshot_last_time = 0
        self.deliver_price = 0

    def on_update(self, timestamp, update: exchange_pb2.InstrumentUpdate):
        """Merges data in the argument update to the local POB."""
        t0 = time.time()
        self.pob.deliver_price = update.deliver_price
        for record in update.bid_quotes:
            self.pob.update_level(
                timestamp, BID, record.price,
                record.volume, record.order_count
            )
        for record in update.ask_quotes:
            self.pob.update_level(
                timestamp, ASK, record.price,
                record.volume, record.order_count
            )

        for trade in update.trades:
            self.pob.add_trade(trade.timestamp, trade.price, trade.volume)

        elapsed = timestamp - self._last_snapshot_time
        if not self.snapshots or elapsed >= self._snapshot_interval:
            self.snapshots.append(self.pob.get_snapshot())
            self._last_snapshot_time = timestamp

        elapsed = timestamp - self._history_snapshot_last_time
        if self.snapshots and elapsed >= self._history_snapshot_interval:
            self._history_snapshot_last_time = timestamp
            return (self.snapshots[-1])

        return None

        dt = time.time() - t0
        print('########## ', dt)


class MarketData(pb2_grpc.MarketDataServicer):
    """Implements core functions of the Market Data module.

    Receives market data from the Exchange and stores the data locally.

    The idea is, the updates pushed by the Exchange are (mostly) incremental. The
    MarketData maintains complete, up-to-date snapshot using one PseudoOrderBook
    object for each instrument. After each fixed, configurable, time interval,
    it takes a snapshot of all PseudoOrderBooks and appends the snapshot to a
    deque of historic snapshots.
    """

    def __init__(self, port, exchange_endpoint=None, exchange_obj=None):
        self._is_started = False

        if exchange_obj:
            # Access Exchange object in local memory
            self._exchange = exchange_obj
        elif exchange_endpoint:
            # Access remote Exchange through gRPC stub
            self._exchange = ExchangeStub(grpc.insecure_channel(exchange_endpoint))
        else:
            raise ValueError("Exchange not specified when init Broker.")

        self._update_interval = 0.1  # seconds

        # Gets instrument list from the Exchange.
        self._instruments = {
            info.symbol: _InstrumentData(info, self._update_interval)
            for info in self._exchange.list_instruments(Empty()).instruments
        }

        # gRPC server
        self._server = None
        self._port = port

        self._updater = threading.Thread(target=self._handle_exchange_updates)
        self._data_available = threading.Event()

        self._history_snapshot_list = []
        self._history_snapshot_size_threshold = 5000
        self._history_snapshot_dump_file_name = 'dump/obsnapshots_@time.json'
        self._serialize = serialize.JsonSerializer(compress=True)  # compress the history file

    def start(self):
        """Creates and starts a server that hosts this Broker servicer."""
        if self._is_started:
            raise NotImplementedError

        self._is_started = True
        self._updater.start()

        self._server = grpc.server(futures.ThreadPoolExecutor())
        pb2_grpc.add_MarketDataServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

    def stop(self):
        """Stops the server that hosts this Broker servicer."""
        if not self._is_started:
            raise NotImplementedError

        # Stops publishing and prevents new subscriptions
        self._is_started = False

        if self._server:
            self._server.stop(0).wait()
            del self._server
            self._server = None

    # MarketDataServicer API:

    def list_instruments(self, request, _=None):
        """(API) Returns static properties of the instruments in the exchange."""
        response = common_pb2.InstrumentInfoList()
        response.instruments.extend([common_pb2.InstrumentInfo(
            symbol=inst.symbol,
            init_price=inst.init_price,
            tick=inst.tick
        ) for inst in self._instruments.values()])

        return response

    def subscribe(self, request: Empty, context=None):
        """(API) Obtains a response stream where latest market snapshots are
        feeded with fixed interval."""
        while self._is_started:
            # Wait until there are data...
            if not self._data_available.wait(0.1):
                continue

            yield self._get_response()
            time.sleep(self._update_interval)

    # Internal functions

    def _handle_exchange_updates(self):
        """Main logic of the updater thread."""
        feed = self._exchange.subscribe_market(Empty())
        for market_update in feed:
            # 遍历完不就退出了？不会遍历完
            if not self._is_started:
                break

            for inst_update in market_update.instruments:
                instpob = self._instruments[inst_update.symbol].on_update(
                    market_update.timestamp, inst_update
                )
                # if instpob:
                # self._save_snapshot_to_history(instpob)

            self._data_available.set()

    def _get_response(self):
        """Creates a MarketSnapshot response with latest instrument snapshots."""
        response = pb2.MarketSnapshot(is_incremental=False)
        for data in self._instruments.values():
            if len(data.snapshots) < 1:
                continue

            src = data.snapshots[-1]
            dst = response.instruments.add()

            dst.symbol = src.symbol
            dst.timestamp = src.timestamp
            dst.last_price = src.last_price
            dst.deliver_price = src.deliver_price
            dst.traded_volume = src.traded_volume
            dst.bid_volume = src.bid_volume
            dst.ask_volume = src.ask_volume
            dst.bid_order_count = src.bid_order_count
            dst.ask_order_count = src.ask_order_count
            dst.bid_depth = src.bid_depth
            dst.ask_depth = src.ask_depth
            dst.bid_levels.extend([
                QuoteRecordType(
                    price=level[0], volume=level[1], order_count=level[2]
                )
                for level in src.bid_levels
            ])
            dst.ask_levels.extend([
                QuoteRecordType(
                    price=level[0], volume=level[1], order_count=level[2]
                )
                for level in src.ask_levels
            ])
            dst.last_trades.extend([
                TradeRecordType(
                    timestamp=trade[0], price=trade[1], volume=trade[2]
                )
                for trade in src.last_trades
            ])

        return response

    def __del__(self):
        print('[MarketData] dump obsnapshots before leave.')
        if self._history_snapshot_list:
            fn = self._history_snapshot_dump_file_name.replace(
                '@time', time.strftime('%Z_%Y%m%d_%H-%M-%S', time.localtime()))
            self._serialize.to_file(self._history_snapshot_list, fn, no_blocking=True)
            del self._history_snapshot_list[:]

    def _save_snapshot_to_history(self, snapshot: pb2.MarketSnapshot):
        """Save snapshot to history

        Serialize history to file when its size exceeds threshold.
        """
        self._history_snapshot_list.append(snapshot)
        if len(self._history_snapshot_list) >= self._history_snapshot_size_threshold:
            # serialize to file with current time in name
            fn = self._history_snapshot_dump_file_name.replace(
                '@time', time.strftime('%Z_%Y%m%d_%H-%M-%S', time.localtime()))
            # serialize history data without blocking current execution
            self._serialize.to_file(self._history_snapshot_list, fn, no_blocking=True)
            # empty history list
            del self._history_snapshot_list[:]
