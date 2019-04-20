"""
Peacock Broker Module.

Manages trader accounts, serves as a delegate between traders and the
Exchange.

For more details, see the README.
"""

import time
import glob
import pickle
import pprint
import threading
import xml.etree.ElementTree as ElementTree
from collections import deque, namedtuple, defaultdict
from concurrent import futures
from random import randint
from datetime import datetime
from .BrokerPostServer import BrokerPostServer

import grpc
import math

from .._pyprotos import broker_admin_pb2 as admin_pb2
from .._pyprotos import broker_admin_pb2_grpc as admin_pb2_grpc
from .._pyprotos import broker_pb2 as pb2
from .._pyprotos import broker_pb2_grpc as pb2_grpc
from .._pyprotos import common_pb2, exchange_pb2
from .._pyprotos.common_pb2 import (
    Empty, RpcResponse,
    ASK, BID, LONG, SHORT, NEW_ORDER, CANCEL_ORDER, INCREMENTAL_INFO, FULL_INFO,
    ORDER_ACCEPTED, ORDER_CANCELLED, ORDER_FINISHED, ORDER_TRADED,
    OK, SERVICE_UNAVAILABLE, REGISTER_DISABLED, ACCOUNT_DISABLED,
    UNAUTHORIZED, TOO_MANY_REQUESTS, TOO_MANY_ORDERS, INVALID_TRADER_NAME, INVALID_TRADER_ID,
    INVALID_PRICE, INVALID_SYMBOL, INVALID_SIDE, INVALID_POSITION,
    INVALID_VOLUME, INVALID_ORDER_ID, INVALID_REQUEST,
    INSUFFICIENT_ASSETS, ON_MARGIN_CALL
)
from .._pyprotos.exchange_pb2_grpc import ExchangeStub
from ..common import Limits, exporter
from ..common.recipes import Incrementer
from ..common.sortedcontainers import SortedDict
from ..common import serialize

from .fees import Fees
from .trader import Trader, TraderStatus


################################################################################
# Broker
################################################################################

# Used to track historical changes of a Trader's assets.
TraderSnapshot = namedtuple('TraderSnapshot', [
    'timestamp', 'is_alive', 'total_cash', 'locked_cash', 'occupied_cash',
    'unrealized_pnl', 'realized_pnl', 'commission'
])
_AccountSnapshot = namedtuple('_AccountSnapshot', [
    'traderid', 'timestamp', 'is_alive',
    'unrealized_pnl', 'realized_pnl', 'commission',
    'pnl', 'IR', 'maxdd', 'mc'
])


class ContestantStats:
    def __init__(self):
        self.rpc_count = 0
        self.first_rpc_time = None
        self.order_count = 0
        self.first_order_time = None
        self.ip_addresses = set()

    def __str__(self):
        return 'First order at: %.3f'


class TraderPerf:
    """Tracks a trader's historical performance."""

    def __init__(self, init_cash):
        self.timestamp = 0.0
        self.init_value = init_cash
        self.max_value = init_cash
        self.min_value = init_cash

        self.total_cash = init_cash
        self.unrealized_pnl = 0.0
        self.locked_cash = 0.0
        self.occupied_cash = 0.0
        self.realized_pnl = 0.0
        self.commission = 0.0

        self.max_drawdown = 0.0

        self.pnl_count = 1
        self.pnl_mean = 0.0
        self.pnl_variance = 0.0
        self.pnl_timer = -1
        self.pnl_prev = 0.0
        self.ir = 0.0
        self.pnl_check = 0.0

    @property
    def pnl(self):
        data = self.total_cash + self.unrealized_pnl - self.init_value
        if math.isfinite(data):
            return data
        else:
            return 0

    @property
    def IR(self):
        if self.pnl_timer < 0:
            self.pnl_timer = self.timestamp + 60
            self.ir = 0.0
        elif self.timestamp >= self.pnl_timer:
            self.pnl_timer += 60
            current_pnl = self.pnl
            diff = current_pnl - self.pnl_prev
            self.ir = self.getIR(diff)
            self.pnl_check += diff
            if self.pnl_check - current_pnl != 0:
                print('interval pnl error:', self.timestamp, self.pnl_check, current_pnl)
            self.pnl_prev = current_pnl
        return self.ir

    def getIR(self, data):
        if self.pnl_count == 1:
            if math.isfinite(data):
                self.pnl_mean = data
                self.pnl_count += 1
            return 0
        elif self.pnl_count > 1:
            if math.isfinite(data):
                SSE = self.pnl_variance * (self.pnl_count - 2)
                delta = data - self.pnl_mean
                self.pnl_mean += delta / self.pnl_count
                SSE += delta * (data - self.pnl_mean)
                self.pnl_variance = SSE / (self.pnl_count - 1)
                self.pnl_count += 1
            if self.pnl_variance < 1e-5:
                return 0
            else:
                return self.pnl_mean / math.sqrt(self.pnl_variance)

    def update(self, timestamp, total_cash, unrealized_pnl, locked_cash,
               occupied_cash, realized_pnl, commission):
        self.timestamp = timestamp
        self.total_cash = total_cash
        self.unrealized_pnl = unrealized_pnl
        self.locked_cash = locked_cash
        self.occupied_cash = occupied_cash
        self.realized_pnl = realized_pnl
        self.commission = commission

        total_value = total_cash + unrealized_pnl

        if total_value < self.min_value:
            self.min_value = total_value
        elif total_value > self.max_value:
            self.max_value = total_value

        draw_down = (self.max_value - total_value) / self.max_value
        if draw_down > self.max_drawdown:
            self.max_drawdown = draw_down


class Broker(pb2_grpc.BrokerServicer, admin_pb2_grpc.BrokerAdminServicer):
    """Broker module implementation.

    Implementing the API defined in ../protos/broker.proto, the Broker
    maintains the trader accounts and serves as a delegate between
    individual traders and the Exchange.

    The Broker communicates with the Exchange through the Exchange's API.
    """
    class Config:
        """Configuration for Broker."""

        def __init__(self, config_name):
            import os.path as path
            full_path = path.join(path.dirname(__file__), config_name + '.xml')
            root = ElementTree.parse(full_path).getroot().find('broker')

            self.broker_id = int(root.get('id'))
            self.name = root.get('name')
            self.pin_length = int(root.get('pin_length', 4))
            self.allows_register = (root.get('allows_register') == 'true')
            self.max_trader_name_length = 32
            self.thread_count = int(root.get('thread_count', 0))
            margin_rate = float(root.get('margin_rate', 1.0))

            self.init_cash = None
            node = root.find('default_account')
            if node is not None:
                self.init_cash = float(node.get('cash', 0))

            self.fees = Fees()
            node = root.find('commission')
            if node is not None:
                self.fees = Fees(
                    commission_rate=float(node.get('rate', 0)),
                    margin_rate=margin_rate
                )

            # Parse initial accounts
            self.init_name_pins = []
            node = root.find('accounts')
            if node is not None:
                for acc_node in node.findall('account'):
                    name = acc_node.get('name')
                    pin = acc_node.get('pin')
                    self.init_name_pins.append((name, pin))

    def __init__(self, config_name, port, admin_port, exchange_endpoint=None, exchange_obj=None):
        self._config = Broker.Config(config_name)
        self._is_started = False
        self.robot_broker_id = 101

        # Init an Exchange stub that is shared by _OrderSubmitter and
        # _ExchangeListener threads.
        if exchange_obj:
            # Object in local memory
            self._exchange = exchange_obj
        elif exchange_endpoint:
            self._exchange = ExchangeStub(grpc.insecure_channel(exchange_endpoint))
        else:
            raise ValueError("Exchange not specified when init Broker.")

        # Gets instrument list from the Exchange.
        self._instruments = {
            info.symbol: info
            for info in self._exchange.list_instruments(Empty()).instruments
        }

        self._traders = {}   # trader ID -> Trader
        self._trader_locks = defaultdict(threading.Lock)

        self._trader_perfs = {}  # trader ID -> TraderPerf
        self._trader_rpc_counts = defaultdict(int)

        # Makes sure messages from the Exchange are handled in batches sequentially.
        self._batch_handler_lock = threading.Lock()
        self._next_batch_id = 0
        self._batched_responses = SortedDict()

        self._prices = {
            symbol: info.last_price
            for symbol, info in self._instruments.items()
        }

        self._start_time = datetime.utcnow().timestamp()

        # gRPC servers.
        self._server = None
        self._port = port

        # self._admin_server = None
        # self._admin_port = admin_port

        # Thread-safe ID generators
        self._order_id = Incrementer()
        self._trader_id = Incrementer()

        self._margin_call_threshold = 10
        self._max_force_close_volume = 1000
        self._next_update_time = 0
        self._auto_update_interval = 0.05   # 20 Hz
        self._auto_updater = threading.Thread(target=self._update_accounts)

        # trader symbol market make complete percent
        self._trader_symbol_mmcp = defaultdict(dict)

        # Create initial accounts (if any)
        for name_pin in self._config.init_name_pins:
            trader_ = Trader(
                trader_id=int(name_pin[0]),
                name=name_pin[0],
                pin=name_pin[1],
                init_cash=self._config.init_cash,
                fees=self._config.fees,
                batch_mode=True
            )

            print(config_name, name_pin[0], name_pin[1], trader_.trader_id)
            self._traders[trader_.trader_id] = trader_
            self._trader_perfs[trader_.trader_id] = TraderPerf(self._config.init_cash)

        # Keeps track of contestants' statistics
        self._contestants = {}      # trader_id -> ContestantStats
        self._peer_rpc_counts = {}  # IP -> int
        self._contest_log_lock = threading.Lock()

        self._history_snapshot_list = []
        self._history_snapshot_size_threshold = 10000
        self._history_snapshot_dump_file_name = 'dump/accounts_@time.json'
        self._serialize = serialize.JsonSerializer(compress=True)  # compress the history file

        self.ip_last_call_ts = defaultdict(int)
        self.trader_id_last_call_ts = defaultdict(int)
        if config_name == 'robot':
            self.post_server = None
        else:
            self.post_server = BrokerPostServer('0.0.0.0', 51100 + (self._port % 100), self)

    def _update_accounts(self):
        """
        Pulls pending take-away messages from the Exchange even when no
        order is happening. Detects traders' available cash and, if necessary,
        issues margin calls.
        """
        while self._is_started:
            timestamp = self.timestamp
            if timestamp >= self._next_update_time:
                self._next_update_time = timestamp + self._auto_update_interval

                deliveries = self._exchange.fetch_deliver_price(exchange_pb2.BrokerRequest(
                    broker_id=self._config.broker_id))

                # Fetched updates may include price changes and asynchronous
                # order events.
                result = self._exchange.fetch_updates(
                    exchange_pb2.BrokerRequest(
                        broker_id=self._config.broker_id,
                        request_type=common_pb2.INCREMENTAL_INFO
                    )
                )

                self._handle_exchange_response(result)

                # Check each trader account
                for trader_id, trader_ in self._traders.items():
                    if trader_.status == TraderStatus.DISABLED:
                        continue

                    trader_.deliver(deliveries.deliveries)

                    # Make sure properties are up-to-date
                    trader_.update_summary()

                    if trader_.available_cash < self._margin_call_threshold:
                        # Try to make some available cash by force
                        actionable = self._margin_call(trader_id)
                        if not actionable:
                            trader_.status = TraderStatus.DISABLED
                    elif trader_.status == TraderStatus.MARGIN_CALL:  # reset reborn here for robots
                        # Restores account activeness
                        trader_.status = TraderStatus.NORMAL

                    # Update the Trader's account performance
                    self._trader_perfs[trader_id].update(
                        timestamp, trader_.total_cash, trader_.unrealized_pnl,
                        trader_.locked_cash, trader_.occupied_cash,
                        trader_.realized_pnl, trader_.commission
                    )

                    if self._config.broker_id != self.robot_broker_id:
                        self._update_accounts_snapshot(trader_id, trader_.get_update(False))
            else:
                # No need to update now
                time.sleep(self._next_update_time - timestamp)

    def _margin_call(self, trader_id):
        """Performs necessary actions when a Trader's available cash is
        below a threshold.
        """
        trader = self._traders[trader_id]
        trader.status = TraderStatus.MARGIN_CALL

        with self._trader_locks[trader_id]:
            actionable = False

            # Cancel all orders, including close orders (because we will
            # close all positions at market price)
            order_ids = trader.get_order_ids()
            for order_id in order_ids:
                symbol = trader.get_order_symbol(order_id)
                self._cancel_order(symbol, trader_id, order_id)
                actionable = True

            if actionable:
                # Continues only if no order can be cancelled
                return True

            # Forcefully close some position (one portion at a time)
            closeable_pos = trader.get_closeable_position()
            if closeable_pos:
                symbol, pos_type, volume = closeable_pos

                # Place an order accordingly
                volume = min(volume, self._max_force_close_volume)
                side = BID if (pos_type == SHORT) else ASK

                self._new_order(symbol, trader_id, side, pos_type, None, volume)

                return True

            return False

    @property
    def timestamp(self):
        """Returns the current timestamp of the Broker.

        Currently it equals to seconds elapsed since the Broker started.
        """
        return datetime.utcnow().timestamp() - self._start_time

    def start(self):
        """Starts the Broker module."""
        if self._is_started:
            raise NotImplementedError('Re-starting is not supported yet')

        self._server = grpc.server(futures.ThreadPoolExecutor(
            max_workers=self._config.thread_count
        ))
        pb2_grpc.add_BrokerServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

        # self._admin_server = grpc.server(futures.ThreadPoolExecutor())
        # admin_pb2_grpc.add_BrokerAdminServicer_to_server(self, self._admin_server)
        #
        # self._admin_server.add_insecure_port('[::]:%d' % self._admin_port)
        # self._admin_server.start()

        if self.post_server is not None:
            self.post_server.start()

        self._is_started = True

        self._auto_updater.start()

    def stop(self):
        """Stops the Broker module."""
        if not self._is_started:
            raise NotImplementedError('Broker is not started')

        # Stops accepting more requests
        self._is_started = False

        if self._server:
            self._server.stop(0)

        # if self._admin_server:
        #     self._admin_server.stop(0)

    ### BrokerServicer API ###################################################

    def info(self, request: common_pb2.Empty, _=None):
        """(API) Returns ID and name of this Broker."""
        return pb2.BrokerInfo(
            id=self._config.broker_id,
            name=self._config.name
        )

    def register(self, request: pb2.RegisterRequest, _=None):
        """(API) Registers a new trader with given name.

        Returns:
            The global ID of the newly registered trader.
        """
        # Validate request...
        if not self._is_started:
            return self._create_trader_response(result_code=SERVICE_UNAVAILABLE)
        if not self._config.allows_register:
            return self._create_trader_response(result_code=REGISTER_DISABLED)
        if not 0 < len(request.trader_name) <= self._config.max_trader_name_length:
            return self._create_trader_response(result_code=INVALID_TRADER_NAME)

        # If the Broker has default account, apply it to the new trader.
        # Otherwise, use the info provided in request.
        init_cash = self._config.init_cash or request.init_cash

        # If no PIN is provided, a random one will be generated.
        trader = Trader(
            trader_id=self._trader_id.next(),
            name=request.trader_name,
            pin=request.trader_pin or self._generate_pin(),
            init_cash=init_cash,
            fees=self._config.fees,
            batch_mode=True
        )
        print('register', self._config.broker_id, trader.trader_id, trader.name, trader.pin)

        # We do not want to interrupt batch processing
        with self._batch_handler_lock:
            self._traders[trader.trader_id] = trader
            self._trader_perfs[trader.trader_id] = TraderPerf(init_cash)

        with self._trader_locks[trader.trader_id]:
            return self._create_trader_response(trader, incremental=False)

    def get_trader(self, request: pb2.TraderRequest, _=None):
        """(API) Returns incremental or full update of a trader."""
        if not self._is_started:
            return self._create_trader_response(result_code=SERVICE_UNAVAILABLE)

        trader = self._traders.get(request.trader_id)

        # Authentication

        if not trader:
            return self._create_trader_response(result_code=INVALID_TRADER_ID)

        if request.trader_pin != trader.pin:
            return self._create_trader_response(result_code=UNAUTHORIZED)

        with self._trader_locks[request.trader_id]:
            # Update account summary
            trader.update_summary()

            if request.request_type == INCREMENTAL_INFO:
                result = self._create_trader_response(trader, incremental=True)
                return result
            elif request.request_type == FULL_INFO:
                return self._create_trader_response(trader, incremental=False)
            else:
                return self._create_trader_response(result_code=INVALID_REQUEST)

    # To refactor
    def _get_peer_ip(self, context):
        fields = context.peer().split(':')
        if len(fields) == 3:
            return fields[1].strip()
        return None

    def new_order(self, request: pb2.TraderRequest, context=None):
        """(API) Adds a new order to the Exchange.

        The Broker checks the validity of the incoming order, such as whether
        the trader account has sufficient assets, before actually delivering
        the order to the Exchange. For a valid order, the Broker also locks
        the appropriate assets in the trader account.
        """
        if not self._is_started:
            return self._create_trader_response(result_code=SERVICE_UNAVAILABLE)

        if context:
            # RPC from remote client
            ip = self._get_peer_ip(context)
            if ip not in self._peer_rpc_counts:
                with self._contest_log_lock:
                    if ip not in self._peer_rpc_counts:
                        self._peer_rpc_counts[ip] = 0
            self._peer_rpc_counts[ip] += 1

        # Authentication

        trader_ = self._traders.get(request.trader_id)

        if not trader_:
            return self._create_trader_response(result_code=INVALID_TRADER_ID)

        if request.trader_pin != trader_.pin:
            return self._create_trader_response(result_code=UNAUTHORIZED)

        with self._trader_locks[request.trader_id]:

            self._trader_rpc_counts[request.trader_id] += 1

            # Update statistics for contestant
            if request.trader_id not in self._contestants:
                with self._contest_log_lock:
                    self._contestants[request.trader_id] = ContestantStats()
            stats = self._contestants[request.trader_id]
            if stats.rpc_count == 0:
                stats.first_rpc_time = self.timestamp
            stats.rpc_count += 1

            if context:
                stats.ip_addresses.add(self._get_peer_ip(context))

            # Check account status

            if trader_.status == TraderStatus.MARGIN_CALL:
                return self._create_trader_response(trader_, result_code=ON_MARGIN_CALL)
            elif trader_.status == TraderStatus.DISABLED:
                return self._create_trader_response(trader_, result_code=ACCOUNT_DISABLED)

            if self._config.broker_id != self.robot_broker_id and trader_.active_order_count >= Limits.MAX_ACTIVE_ORDERS:
                return self._create_trader_response(trader_, result_code=TOO_MANY_ORDERS)

            # Check order parameters

            if request.request_type != NEW_ORDER:
                return self._create_trader_response(trader_, result_code=INVALID_REQUEST)

            if request.symbol not in self._instruments:
                return self._create_trader_response(trader_, result_code=INVALID_SYMBOL)

            if request.side != BID and request.side != ASK:
                return self._create_trader_response(trader_, result_code=INVALID_SIDE)

            if request.pos_type != LONG and request.pos_type != SHORT:
                return self._create_trader_response(trader_, result_code=INVALID_POSITION)

            if not self._is_price_valid(request):
                return self._create_trader_response(trader_, result_code=INVALID_PRICE)

            if self._config.broker_id != self.robot_broker_id and not Limits.is_volume_valid(request.volume):
                return self._create_trader_response(trader_, result_code=INVALID_VOLUME)

            # Round limit order price by instrument's price tick
            order_price = self._clipped_price(request)

            result_code = self._new_order(
                request.symbol, request.trader_id, request.side,
                request.pos_type, order_price, request.volume
            )

            if result_code == OK:
                if stats.order_count == 0:
                    stats.first_order_time = self.timestamp
                stats.order_count += 1

            result = self._create_trader_response(trader_, result_code=result_code)
            return result

    def cancel_order(self, request: pb2.TraderRequest, _=None):
        """(API) Cancels an order."""
        if not self._is_started:
            return self._create_trader_response(result_code=SERVICE_UNAVAILABLE)

        trader_ = self._traders.get(request.trader_id)

        # Authentication
        if not trader_:
            return self._create_trader_response(result_code=INVALID_TRADER_ID)

        if request.trader_pin != trader_.pin:
            return self._create_trader_response(result_code=UNAUTHORIZED)

        self._trader_rpc_counts[request.trader_id] += 1
        with self._trader_locks[request.trader_id]:
            if trader_.status == TraderStatus.MARGIN_CALL:
                return self._create_trader_response(trader_,
                                                    result_code=ON_MARGIN_CALL
                                                    )
            elif trader_.status == TraderStatus.DISABLED:
                return self._create_trader_response(trader_,
                                                    result_code=ACCOUNT_DISABLED
                                                    )

            # Check request parameters

            if request.request_type != CANCEL_ORDER:
                return self._create_trader_response(trader_,
                                                    result_code=INVALID_REQUEST
                                                    )

            symbol = trader_.get_order_symbol(request.order_id)
            if not symbol:
                return self._create_trader_response(trader_,
                                                    result_code=INVALID_ORDER_ID
                                                    )

            self._cancel_order(symbol, request.trader_id, request.order_id)

            result = self._create_trader_response(trader_)
            return result

    def _new_order(self, symbol, trader_id, side, pos_type, price, volume):
        """Places a new order for a trader. Returns a ResultCode."""
        order_id = self._order_id.next()  # Increment global order ID

        trader_ = self._traders[trader_id]

        order_added = trader_.add_order(
            order_id, side, symbol, volume, price, self._prices[symbol],
            pos_type
        )

        if not order_added:
            return INSUFFICIENT_ASSETS

        # Submit order to Exchange and get result
        result = self._exchange.new_order(exchange_pb2.BrokerRequest(
            broker_id=self._config.broker_id,
            request_type=NEW_ORDER,
            trader_id=trader_id,
            order_id=order_id,
            symbol=symbol,
            side=side,
            volume=volume,
            price=price or 0,
            is_market=(price is None),
            pos_type=pos_type
        ))

        self._handle_exchange_response(result)

        # Refresh account summary
        trader_.update_summary()

        return OK

    def _cancel_order(self, symbol, trader_id, order_id):
        """Cancels an order for a trader."""
        result = self._exchange.cancel_order(exchange_pb2.BrokerRequest(
            broker_id=self._config.broker_id,
            request_type=CANCEL_ORDER,
            trader_id=trader_id,
            order_id=order_id,
            symbol=symbol
        ))
        self._handle_exchange_response(result)

        # Refresh account summary
        self._traders[trader_id].update_summary()

    # BrokerAdmin service

    def status(self, request: Empty, _):
        total_value = 0.0
        total_unreal_pnl = 0.0
        total_commission = 0.0
        for perf in self._trader_perfs.values():
            total_value += perf.total_cash + perf.unrealized_pnl
            total_unreal_pnl += perf.unrealized_pnl
            total_commission += perf.commission

        return admin_pb2.BrokerStatus(
            id=self._config.broker_id, name=self._config.name,
            registered_traders=self._trader_id.value,
            order_count=self._order_id.value,
            total_value=total_value,
            total_unrealized_pnl=total_unreal_pnl,
            total_commission=total_commission
        )

    def _list_traders(self):
        response = admin_pb2.TraderSummaryList()
        for trader_id, trader_ in self._traders.items():
            info = response.traders.add()  # broker_admin_pb2.TraderSummary
            info.trader_id = trader_id
            info.name = trader_.name
            info.is_alive = trader_.is_alive
            info.rpc_count = self._trader_rpc_counts[trader_.trader_id]
            info.margin_call_count = trader_.margin_call_count

            perf = self._trader_perfs.get(trader_id)
            if perf:
                info.timestamp = perf.timestamp
                info.total_cash = perf.total_cash
                info.unrealized_pnl = perf.unrealized_pnl
                info.locked_cash = perf.locked_cash
                info.occupied_cash = perf.occupied_cash
                info.realized_pnl = perf.realized_pnl
                info.commission = perf.commission
                info.pnl = perf.pnl
                info.IR = perf.IR
                info.max_drawdown = perf.max_drawdown

        return response

    def list_traders(self, request: Empty, _):
        """(API) Lists brief info of all traders."""
        return self.list_traders()

    # Internal Functions:

    def _generate_pin(self):
        return ''.join((str(randint(0, 9)) for _ in range(self._config.pin_length)))

    def _clipped_price(self, request):
        """Rounds the price with the instrument's price tick."""
        if request.is_market:
            return None

        tick = self._instruments[request.symbol].tick
        return round(request.price / tick) * tick

    def _is_price_valid(self, request):
        """Verifies if the request price is within a valid range."""
        if not request.is_market:
            market_price = self._prices[request.symbol]
            diff_ratio = (request.price - market_price) / market_price
            within_range = abs(diff_ratio) <= Limits.MAX_PRICE_DIFF_RATIO
            if not within_range:
                print('id: %s Market price: %.2f  invalid order price: %.2f' % (
                    request.trader_id, market_price, request.price
                ))
            return within_range
        return True     # market order

    def _handle_exchange_response(self, response):
        """Handles price or order events from the Exchange.

        Specifically, it does the following:
            1. Handle order-related events
                Call each relevant trader's on_order_event().
            2. Handle updated prices
                Update local prices dict and call all traders' on_prices_change().
            3. Prepare and queue take-away messages for each trader
                The message will contain a trader's updated account and orders.

        If the response is not what to be expected (i.e., with a batch ID greater
        than self._next_batch_id), the response will be kept in
        self._batched_responses without processing.

        Returns the number of batches actually handled.

        Args:
            response: exchange_pb2.BrokerResponse
        """
        updated_prices = {}

        # Makes sure responses are handled in strict batch order

        handled_count = 0
        with self._batch_handler_lock:
            self._batched_responses[response.batch_id] = response
            next_response = self._batched_responses.pop(self._next_batch_id, None)

            while next_response:    # exchange_pb2.BrokerResponse
                for trader_info in next_response.traders:
                    for record_info in trader_info.market_records:
                        self._trader_symbol_mmcp[trader_info.trader_id][record_info.symbol] = record_info.percent

                # Handle order events related to this Broker
                for event in next_response.order_events:
                    trader_ = self._traders[event.trader_id]
                    trader_.on_order_event(event.order_id, event.state, event.price, event.volume)

                # Update instrument prices.
                for sym_price in next_response.prices:
                    updated_prices[sym_price.symbol] = sym_price.price

                self._next_batch_id += 1
                handled_count += 1
                next_response = self._batched_responses.pop(self._next_batch_id, None)

            # Update prices and price-related account info
            if updated_prices:
                self._prices.update(updated_prices)
                for trader_ in self._traders.values():
                    trader_.on_prices_change(updated_prices)
        return handled_count

    def _create_trader_response(self, trader_=None, incremental=True, result_code=OK):
        """Constructs a TraderResponse for a trader.

        Args:
            incremental: whether to return incremental or full info
                of the positions and the orders.
        """
        response = pb2.TraderResponse(
            timestamp=self.timestamp, result_code=result_code
        )

        if not trader_:
            return response

        trader_id_ = trader_.trader_id
        if not incremental:
            # Full update also includes static account info
            info = response.info
            info.broker_id = self._config.broker_id
            info.trader_id = trader_id_
            info.trader_pin = trader_.pin
            info.trader_name = trader_.name
            info.commission_rate = trader_.commission_rate
            info.margin_rate = trader_.margin_rate

        update = trader_.get_update(incremental)

        # Account summary
        acc = response.account      # broker_pb2.TraderAccount
        acc.is_alive = update.is_alive
        acc.total_cash = update.total_cash
        acc.unrealized_pnl = update.unrealized_pnl
        acc.locked_cash = update.locked_cash
        acc.occupied_cash = update.occupied_cash
        acc.realized_pnl = update.realized_pnl
        acc.commission = update.commission

        # Long positions
        for sym, pos_update in update.long_positions.items():
            pos = response.positions.long_positions[sym]
            pos.volume = pos_update.volume
            pos.locked_volume = pos_update.locked_volume
            pos.occupied_cash = pos_update.occupied_cash
            pos.avg_price = pos_update.avg_price
            pos.unrealized_pnl = pos_update.unrealized_pnl
            pos.realized_pnl = pos_update.realized_pnl

        # Short positions
        for sym, pos_update in update.short_positions.items():
            pos = response.positions.short_positions[sym]
            pos.volume = pos_update.volume
            pos.locked_volume = pos_update.locked_volume
            pos.occupied_cash = pos_update.occupied_cash
            pos.avg_price = pos_update.avg_price
            pos.unrealized_pnl = pos_update.unrealized_pnl
            pos.realized_pnl = pos_update.realized_pnl

        # Orders
        order_update = response.orders
        for order_id, order in update.orders.items():
            dst = order_update.orders[order_id]
            dst.order_id = order.order_id
            dst.symbol = order.symbol
            dst.side = order.side
            dst.pos_type = order.pos_type
            dst.init_price = order.init_price or 0
            dst.init_volume = order.init_volume
            dst.state = order.state
            dst.volume = order.volume
            dst.avg_price = order.avg_price
            dst.commission = order.commission

        tmp_mmcp = self._trader_symbol_mmcp[trader_id_]
        if tmp_mmcp:
            for symbol, value in tmp_mmcp.items():
                r = response.market_records.add()
                r.symbol = symbol
                r.percent = value

        for symbol, value in trader_.volume_stats.items():
            r = response.volume_records.add()
            r.symbol = symbol
            r.volume = value

        perf = self._trader_perfs.get(trader_id_)
        if perf:
            response.pnl = perf.pnl
        return response

    def _update_accounts_snapshot(self, trader_id, update):
        perf = self._trader_perfs[trader_id]
        mccount = self._traders[trader_id].margin_call_count
        snapshot = _AccountSnapshot(
            traderid=trader_id,
            timestamp=self.timestamp,
            is_alive=update.is_alive,
            unrealized_pnl=update.unrealized_pnl,
            realized_pnl=update.realized_pnl,
            commission=update.commission,
            pnl=perf.pnl,
            IR=perf.IR,
            maxdd=perf.max_drawdown * 100,
            mc=mccount,
        )
        self._save_snapshot_to_history(snapshot)
        # pprint.pprint(snapshot)

    def __del__(self):
        print('[broker] dump accounts before leave.')
        if self._history_snapshot_list:
            fn = self._history_snapshot_dump_file_name.replace(
                '@time', time.strftime('%Z_%Y%m%d_%H-%M-%S', time.localtime()))
            self._serialize.to_file(self._history_snapshot_list, fn, no_blocking=True)
            del self._history_snapshot_list[:]

    def _save_snapshot_to_history(self, snapshot: _AccountSnapshot):
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

    def dump_trader_info(self):
        array_result = []
        for tid, trader_ in self._traders.items():
            single_result = {
                'trader_id': trader_.trader_id,
                'name': trader_.name,
                'pin': trader_.pin,
                'broker': self._config.name
            }
            market_records = {}
            if tid in self._trader_symbol_mmcp:
                tmp_mmcp = self._trader_symbol_mmcp[tid]
                for symbol, value in tmp_mmcp.items():
                    if value > 0.0:
                        market_records[symbol] = value

            if len(market_records) > 0:
                single_result['market_records'] = market_records
            if 'all' in market_records:
                single_result['market_all'] = market_records['all']
            else:
                single_result['market_all'] = 0.0

            volume_records = {}
            for symbol, value in trader_.volume_stats.items():
                if value > 0:
                    volume_records[symbol] = value

            if len(volume_records) > 0:
                single_result['volume_records'] = volume_records
            if 'all' in volume_records:
                single_result['volume_all'] = volume_records['all']
            else:
                single_result['volume_all'] = 0.0

            perf = self._trader_perfs.get(tid)
            if perf and abs(perf.pnl) > 0.0:
                single_result['pnl'] = perf.pnl
            else:
                single_result['pnl'] = 0.0

            array_result.append(single_result)
        return array_result
