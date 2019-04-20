"""
Based on PyLOB by Ash Booth
"""

import bisect
from collections import namedtuple
import time
from datetime import datetime
from pathlib import Path
import os

from .._pyprotos.common_pb2 import ASK, BID


################################################################################
# OrderBook with order matching engine
################################################################################

TradeRecord = namedtuple('TradeRecord', [
    'price', 'volume',
    'bid_broker_id', 'bid_trader_id', 'bid_order_id', 'bid_order_remains',
    'ask_broker_id', 'ask_trader_id', 'ask_order_id', 'ask_order_remains'
])
TradeRecord.__doc__ = """Record of a single trading transaction."""


QuoteRecord = namedtuple('QuoteRecord', [
    'side', 'price', 'volume', 'order_count'
])
QuoteRecord.__doc__ = """A tuple of price, volume, and order count."""


class OrderBook:
    """Implements a Limited Order Book (LOB) for one instrument.

    The OrderBook is internal to Exchange, and should only be directly
    accessed by an Exchange object.
    The OrderBook may change the volume of the orders. But it does not
    change order status.

    This class is not thread-safe.

    Attributes:
        last_price: Latest trading price.
        last_volume: Latest total traded volume.
        last_trades: A deque containing the latest N processed trades.
        last_orders: A deque containing the latest N incoming orders.
    """

    def __init__(self, init_price, price_tick, symbol=None):
        self._symbol = symbol
        self._last_price = init_price
        if symbol is not None:
            base = str(Path(__file__).resolve().parents[2])
            _price_filename = "{}_price.{}.log".format(symbol, time.strftime("%Y%m%d_%H%M"))
            _price_filename = os.path.join(base, _price_filename)
            self._price_file = open(_price_filename, 'w')
            self._price_file.write('{} {}\n'.format(self._last_price, datetime.now().strftime("%H%M%S%f")[:-3]))
        self._tick = price_tick
        self._traded_volume = 0
        self._added_order_count = 0
        self._removed_order_count = 0
        self._bids = _OrderTree()
        self._asks = _OrderTree()

    @property
    def bids(self):
        return self._bids

    @property
    def asks(self):
        return self._asks

    @property
    def last_price(self):
        """Latest trading price."""
        return self._last_price

    @property
    def traded_volume(self):
        """Returns the total volume of traded amount."""
        return self._traded_volume

    @property
    def added_order_count(self):
        """Total number of orders ever added to this orderbook.

        Including cancelled and finished orders.
        """
        return self._added_order_count

    @property
    def removed_order_count(self):
        """Total number of orders removed from this orderbook."""
        return self._removed_order_count

    @property
    def bid_order_count(self):
        """Total number of orders on the bid side."""
        return self._bids.order_count

    @property
    def ask_order_count(self):
        """Total number of orders on the ask side."""
        return self._asks.order_count

    def new_order(self, broker_id, trader_id, order_id,
                  side, price, volume):
        """Processes a new order and returns the matched trades (if any).

        The function matches the incoming order to the appropriate order(s)
        in the book. When a trade can be executed, the volume of the two
        matching orders will be changed accordingly. Completed fulfilled
        orders will be removed from the book.

        Caller to this function (i.e., the Exchange object) should check
        the returned Trade object list and handle change of volumes in the
        orders.

        Returns:
            A tuple (trades, quotes, left_cancelled) where:
                `trades` is a list of fulfilled TradeRecords
                `quotes` is a list of updated QuoteRecords
                `left_cancelled` is True if a market order cannot be fully
                    traded and the remaining part is cancelled.
        """
        assert (price is None or price > 0) and volume > 0

        order = _Order(
            broker_id=broker_id,
            trader_id=trader_id,
            order_id=order_id,
            side=side,
            price=price,
            volume=volume
        )
        self._added_order_count += 1

        if order.price:
            # Round to price tick
            order.price = self._clipped_price(order.price)

            return self._process_limit_order(order)
        else:
            return self._process_market_order(order)

    def remove_order(self, broker_id, order_id):
        """Removes an order with the given ID from the LOB.

        Does not change order status.

        If the order is found and removed, returns a QuoteRecord to
        reflect the quote after the order is removed.
        Otherwise, returns None.
        """
        order_node = None
        internal_id = _Order.get_internal_id(broker_id, order_id)

        if internal_id in self._bids.order_nodes:
            order_node = self._bids.order_nodes[internal_id]
        elif internal_id in self._asks.order_nodes:
            order_node = self._asks.order_nodes[internal_id]
        else:
            # Order does not exist. probably already traded.
            return None

        # Sanity check
        order = order_node.order
        assert order.broker_id == broker_id
        assert order.order_id == order_id

        side, price = order.side, order.price

        order_node.remove_from_book()
        self._removed_order_count += 1

        return self._quote_at(side, price)

    def close(self):
        if self._symbol:
            self._price_file.close()

    def _process_limit_order(self, order):
        """Handles an incoming limit order."""
        trades = []
        quotes = []
        if order.side == BID:
            while (order.volume > 0 and not self._asks.is_empty and
                   self._asks.min_price <= order.price):
                # Match incoming order with optimal counterparty orders.
                trades += self._match_trades(order, self._asks.min_priced_list())
                quotes.append(self._quote_at(ASK, self._last_price))

            # If volume remains, add to book
            if order.volume > 0:
                self._bids.add_order(order)
                quotes.append(self._quote_at(BID, order.price))
        else:  # order.side == ASK:
            while (order.volume > 0 and not self._bids.is_empty and
                   self._bids.max_price >= order.price):
                # Match incoming order with optimal counterparty orders.
                trades += self._match_trades(order, self._bids.max_priced_list())
                quotes.append(self._quote_at(BID, self._last_price))

            # If volume remains, add to book
            if order.volume > 0:
                self._asks.add_order(order)
                quotes.append(self._quote_at(ASK, order.price))

        return trades, quotes, False

    def _process_market_order(self, order):
        """Handles an incoming market order."""
        trades = []
        quotes = []
        if order.side == BID:
            while order.volume > 0 and not self._asks.is_empty:
                trades += self._match_trades(order, self._asks.min_priced_list())
                quotes.append(self._quote_at(ASK, self._last_price))

        else:  # order.side == ASK:
            while order.volume > 0 and not self._bids.is_empty:
                trades += self._match_trades(order, self._bids.max_priced_list())
                quotes.append(self._quote_at(BID, self._last_price))

        return trades, quotes, (order.volume > 0)

    def _match_trades(self, order, order_list):
        """Matches an order with counterparty orders in an _OrderList.

        If a matching trade can be made, the function updates the remaining
        volume of the incoming Order, as well as those in the _OrderList.

        Args:
            order: The incoming order to be matched.
            order_list: The _OrderList that can be matched with the incoming
                order.

        Returns:
            A list of matched trades.
        """
        self._last_price = order_list.price  # We're sure some trade will be made
        if self._symbol:
            self._price_file.write('{} {}\n'.format(self._last_price, datetime.now().strftime("%H%M%S%f")[:-3]))
            self._price_file.flush()

        trades = []
        while order.volume > 0 and order_list.volume > 0:
            head_order = order_list.head.order

            trade_volume = min(order.volume, head_order.volume)

            order.volume -= trade_volume
            order_list.head.fulfill_volume(trade_volume)

            self._traded_volume += trade_volume

            if order.side == BID:
                trade = TradeRecord(self._last_price, trade_volume,
                                    order.broker_id, order.trader_id,
                                    order.order_id, order.volume,
                                    head_order.broker_id, head_order.trader_id,
                                    head_order.order_id, head_order.volume)
            else:
                trade = TradeRecord(self._last_price, trade_volume,
                                    head_order.broker_id, head_order.trader_id,
                                    head_order.order_id, head_order.volume,
                                    order.broker_id, order.trader_id,
                                    order.order_id, order.volume)
            trades.append(trade)

        return trades

    def _quote_at(self, side, price):
        """Returns the quote info (volume, order count) at a given price."""
        tree = self._asks if side == ASK else self._bids
        nodes = tree.list_at_price(price)
        if nodes:
            return QuoteRecord(
                side=side,
                price=price,
                volume=nodes.volume,
                order_count=nodes.length)

        return QuoteRecord(side, price, 0, 0)

    def _clipped_price(self, price):
        """Clips the price according to the tick-size."""
        return round(price / self._tick) * self._tick


################################################################################
# Internal data types
################################################################################

class _Order:
    """Order type internal to the Exchange.

    Not to be confused with Broker's Order type, which contains more attributes
    that are irrelevant to the Exchange module.

    Note that while the Exchange module provides an API for generating a new
    order ID (GetNewOrderID), the Exchange does not assign ID to its internal
    Order instance. Instead, the internal Order shares the same ID with the
    external Broker Order.
    """

    def __init__(self, broker_id, trader_id, order_id,
                 side, price, volume):
        self.broker_id = broker_id
        self.trader_id = trader_id
        self.order_id = order_id
        self.side = side
        self.price = price
        self.volume = volume

    @staticmethod
    def get_internal_id(broker_id, order_id):
        """Calculates a unique identifier from a Broker ID and an Order ID."""
        # TODO: replace magic number with configurable parameter
        return order_id * 256 + broker_id

    @property
    def internal_id(self):
        """Unique identifier used internally by the _OrderTree."""
        return _Order.get_internal_id(self.broker_id, self.order_id)


class _OrderNode(object):
    """Wraps an Order object with bidirectional pointers.

    Attributes:
        order: The Order object.
        prev: Previous node in the list.
        next: Next node in the list.
        list: The _OrderList this node belongs to.
    """

    def __init__(self, order):
        self.order = order
        self.prev = None
        self.next = None
        self.list = None

    def remove_from_book(self):
        """Removes this node from the _OrderList it belongs to.

        Calling this function to remove an order from the Order Book ensures
        all the nodes, cached volumes are correctly updated.
        """
        assert self.list is not None
        assert self.list.tree is not None

        # Updates total volume in parent list and tree!
        self.list.volume -= self.order.volume
        self.list.tree.volume -= self.order.volume

        self.list.length -= 1
        del self.list.tree.order_nodes[self.order.internal_id]

        prev_node, next_node = self.prev, self.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node
        elif next_node:  # self is the list head
            next_node.prev = None
            self.list.head = next_node
        elif prev_node:  # self is the list tail
            prev_node.next = None
            self.list.tail = prev_node
        else:            # self is the only one in the list
            self.list.head = None
            self.list.tail = None
            self.list.tree.remove_price(self.list.price)

        self.list = None
        self.prev = None
        self.next = None

    def fulfill_volume(self, volume):
        """Fulfills a certain volume from order in this node."""
        assert 0 < volume <= self.order.volume

        self.order.volume -= volume
        self.list.volume -= volume
        self.list.tree.volume -= volume

        if self.order.volume == 0:
            # Completely fulfilled.
            self.remove_from_book()


class _OrderList:
    """Linked list of orders at the same price in an LOB.

    Attributes:
        price: Price of the order.
        head: First node of the list.
        tail: Last node of the list.
        length: Number of nodes in the list.
        volume: Total share volume of all orders in the list.
    """

    def __init__(self, price, tree):
        self.price = price
        self.tree = tree
        self.volume = 0    # Total share volume
        self.length = 0
        self.head = None
        self.tail = None
        self._iter = None

    def __len__(self):
        return self.length

    def __iter__(self):
        self._iter = self.head
        return self

    def __next__(self):
        if self._iter is None:
            raise StopIteration
        else:
            order = self._iter.order
            self._iter = self._iter.next
            return order

    def append(self, node):
        """Appends an _OrderNode to the tail of the list."""
        assert node.list is None

        node.list = self
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.length += 1
        self.volume += node.order.volume

    def move_to_tail(self, node):
        """Moves a specified node to the tail of the list."""
        assert node.list == self

        if node == self.tail:
            return

        if node == self.head:
            self.head = node.next
        else:
            node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = self.tail
        node.next = None
        self.tail.next = node
        self.tail = node


class _OrderTree:
    """Organizes lists of orders on one side of the LOB.

    The class uses a Red-Black Tree for efficient indexing or order lists
    at different prices. RB-tree ensures that when an optimal price is
    removed (all orders matched), we can get the next optimal price
    efficiently.

    Note: this class is not thread-safe.

    Attributes:
        volume: Keeps track of total volume in this tree.
        prices: Dict of order lists, indexed by price.
        Removed: price_tree: Internal RB-tree for order list indexing.
        order_nodes: Nodes of the unfulfilled orders.
    """

    def __init__(self):
        self.volume = 0   # How much volume on this side?
        self.prices = {}  # price -> _OrderList
        self.order_nodes = {}  # Internal ID -> _OrderNode
        self.sorted_prices = []  # Sorted list of prices

    @property
    def is_empty(self):
        """Returns whether the tree contains no order."""
        return len(self.prices) == 0

    @property
    def order_count(self):
        """Total number of orders."""
        return len(self.order_nodes)

    @property
    def num_prices(self):
        """Returns number of prices in the tree."""
        return len(self.prices)

    @property
    def max_price(self):
        """Returns the highest price in the tree."""
        price = self.sorted_prices[-1] if len(self.prices) > 0 else None
        return price

    @property
    def min_price(self):
        """Returns the lowest price in the tree."""
        price = self.sorted_prices[0] if len(self.prices) > 0 else None
        return price

    def max_priced_list(self):
        """Returns the order list at the highest price."""
        price = self.max_price
        orders = self.prices[price] if price is not None else None
        return orders

    def min_priced_list(self):
        """Returns the order list at the lowest price."""
        price = self.min_price
        orders = self.prices[price] if price is not None else None
        return orders

    def list_at_price(self, price):
        """Returns the order list at the given price."""
        return self.prices[price] if price in self.prices else None

    def max_quotes(self, max_depth: int):
        """Returns quote info (price, volume) at the highest N prices."""
        quotes = [(price, self.prices[price].volume)
                  for price in reversed(self.sorted_prices[-max_depth:])]
        return quotes

    def min_quotes(self, max_depth: int):
        """Returns quote info (price, volume) at the lowest N prices."""
        quotes = [(price, self.prices[price].volume)
                  for price in self.sorted_prices[:max_depth]]
        return quotes

    def add_price(self, price):
        """Adds a new price."""
        assert price not in self.prices

        new_list = _OrderList(price, self)
        self.prices[price] = new_list
        bisect.insort(self.sorted_prices, price)  # keep prices sorted

    def remove_price(self, price):
        """Removes a price and all associated order nodes."""
        assert price in self.prices

        del self.prices[price]
        del self.sorted_prices[bisect.bisect_left(self.sorted_prices, price)]

    def add_order(self, order):
        """Appends a new order to the appropriate price-indexed order list."""
        assert order.internal_id not in self.order_nodes, '%d exists in %s' % (
            order.internal_id, str(self.order_nodes.keys())
        )

        if order.price not in self.prices:
            self.add_price(order.price)

        node = _OrderNode(order)
        self.order_nodes[order.internal_id] = node
        self.prices[order.price].append(node)
        self.volume += order.volume
