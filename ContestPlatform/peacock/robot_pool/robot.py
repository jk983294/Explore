"""
Base class for an internal trading robot.
"""

from collections import defaultdict, namedtuple
from enum import Enum

from .._pyprotos.common_pb2 import (BID, LONG)
from ..client import TradeClient, MarketClient


class SharedInfoKey(Enum):
    """Key used to index info shared among robots."""
    STEP_NUM = 0        # total number of steps in the pool
    SYM_FP = 1          # dict: symbol -> fair_price
    TIME_ELAPSE = 2     # real time elapsed in seconds
    PERIOD = 3          # period in seconds to update fair price
    UPDATE = 4


OrderParams = namedtuple('OrderParams', [
    'side', 'symbol', 'volume', 'price', 'pos_type'
])


class Robot:
    """
    An internal trading robot
    Each robot uses its member variable, self.client, a TradeClient
    instance to perform various trading-related operations
    """

    def __init__(self, shared_info: dict, broker_stub,
                 market_client: MarketClient,
                 name=None, pin=None, xml_node=None):
        self.shared_info = shared_info
        self.trade_client = TradeClient(broker_stub=broker_stub)
        self.market_client = market_client
        self.name = name or "Noname"

        self.reborn_needed = False

        # Statistics
        self.total_order_count = 0
        self.total_cancel_count = 0
        self.result_histogram = defaultdict(int) # ResultCode -> count

        init_cash = None
        if xml_node is not None:
            init_cash = float(xml_node.get('init_cash', 0))

        # Register a new trader (with initial account).
        self.trade_client.register(name, pin, init_cash)

        # Custom initialization
        self.on_init(xml_node)

    def order(self, params: OrderParams, orig_timestamp=None):
        """Places a new order.

        Instead of calling self.trade_client.order(), this is the
        preferred way to place a new order as it will update
        important statistics.
        """
        result_code = self.trade_client.order(
            params.side, params.symbol, params.volume, params.price,
            params.pos_type, orig_timestamp
        )
        if result_code != 0:
            print('[%s] %s %d shares of %s at %.2f in %s position ERROR %d' % (
                self.name, 'buy' if params.side == BID else 'sell',
                params.volume, params.symbol, params.price or 0,
                'long' if params.pos_type == LONG else 'short',
                result_code
            ))

        self.total_order_count += 1     # no matter successful or not
        self.result_histogram[result_code] += 1

        return result_code

    def cancel(self, order_id):
        """
        Cancels an existing order.
        Prefer using this method to cancel order instead of using
        self.trade_client.cancel().
        """
        result_code = self.trade_client.cancel(order_id)

        self.total_cancel_count += 1
        self.result_histogram[result_code] += 1

        return result_code

    def on_init(self, xml_node):
        """Called when the robot is initialized with config XML."""
        pass

    def on_started(self):
        """Called right before the Robot starts running."""
        pass # print('Robot %s started.' % self.name)

    def on_stopped(self):
        """Called right after the Robots stops running."""
        pass # print('Robot %s stopped.' % self.name)

    def on_step(self):
        """Called in every simulation step. Subclasses must override this."""
        raise NotImplementedError
