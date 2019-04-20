"""Pseudo and Static OrderBook classes."""

from collections import deque, namedtuple

from .._pyprotos.common_pb2 import BID
from .sortedcontainers import SortedDict, SortedSet


StaticOrderBook = namedtuple('StaticOrderBook', [
    'symbol', 'timestamp', 'last_price', 'traded_volume', 'last_trades',
    'bid_order_count', 'bid_volume', 'bid_depth', 'bid_levels',
    'ask_order_count', 'ask_volume', 'ask_depth', 'ask_levels', 'deliver_price'
])
StaticOrderBook.__doc__ = """Immutable snapshot of an orderbook."""


class PseudoOrderBook:
    """Contains incomplete info of a real OrderBook.

    It is called "pseudo" because it does not hold detailed order info as a
    "real" orderbook does. It only contains higher-level info such as order
    count, total volume etc. for each price level. It also does not have a
    matching engine.

    Each level is represented by a tuple: (price, volume, order_count)

    The class also keeps track of most recent trade records as a deque of
    simple tuples: (timestamp, price, volume)

    Meant to be used as a dynamic mirror of an OrderBook, allowing clients
    to access the dynamic orderbook data without interferring the order-
    matching process.

    Update the POB by feeding it trade records and price-level updates.

    Not thread-safe.
    """

    def __init__(self, symbol, last_price=0.0, traded_volume=0):
        self._symbol = symbol
        self._last_timestamp = 0.0
        self._last_price = last_price
        self._traded_volume = traded_volume

        # Tracks changes made after last call of reset_changes().
        self._last_trades = deque(maxlen=1000)
        self._last_bid_prices = SortedSet()
        self._last_ask_prices = SortedSet()

        self._bid_levels = SortedDict()   # price -> (volume, order_count)
        self._ask_levels = SortedDict()   # price -> (volume, order_count)

        self._bid_order_count = 0
        self._ask_order_count = 0
        self._bid_volume = 0
        self._ask_volume = 0
        self.deliver_price = 0

    @property
    def symbol(self):
        """Symbol of the instrument."""
        return self._symbol

    @property
    def last_price(self):
        """Latest trade price."""
        return self._last_price

    @property
    def traded_volume(self):
        """Total volume traded."""
        return self._traded_volume

    @property
    def bid_order_count(self):
        """Total number of bid orders in the book."""
        return self._bid_order_count

    @property
    def ask_order_count(self):
        """Total number of ask orders in the book."""
        return self._ask_order_count

    @property
    def total_order_count(self):
        """Total number of bid and ask orders in the book."""
        return self._bid_order_count + self._ask_order_count

    @property
    def bid_volume(self):
        """Total volume of bid orders in the book."""
        return self._bid_volume

    @property
    def ask_volume(self):
        """Total volume of ask orders in the book."""
        return self._ask_volume

    @property
    def total_volume(self):
        """Total volume of both sides currently in the book."""
        return self._bid_volume + self._ask_volume

    @property
    def bid_depth(self):
        """Number of bid price levels."""
        return len(self._bid_levels)

    @property
    def ask_depth(self):
        """Number of ask price levels."""
        return len(self._ask_levels)

    @property
    def bid_levels(self):
        """List of bid levels (price, volume, order_count) sorted descendingly."""
        return [(price, value[0], value[1])
                for price, value in reversed(self._bid_levels.items())]

    @property
    def ask_levels(self):
        """List of ask levels (price, volume, order_count) sorted ascendingly."""
        return [(price, value[0], value[1])
                for price, value in self._ask_levels.items()]

    @property
    def last_trades(self):
        """List of latest trade records (timestamp, price, volume)."""
        return list(self._last_trades)

    def update_level(self, timestamp, side, price, volume, order_count):
        """Updates a certain price level."""
        levels = self._bid_levels if side is BID else self._ask_levels
        old_volume, old_order_count = levels.get(price, (0, 0))

        if volume is 0:
            if price in levels:
                del levels[price]
        else:
            levels[price] = (volume, order_count)

        delta_volume = volume - old_volume
        delta_order_count = order_count - old_order_count

        if side is BID:
            self._bid_volume += delta_volume
            self._bid_order_count += delta_order_count
        else:
            self._ask_volume += delta_volume
            self._ask_order_count += delta_order_count

        self._last_timestamp = max(self._last_timestamp, timestamp)

    def add_trade(self, timestamp, price, volume):
        """Adds a new trade record and update the last trade price and
        total traded volume.
        """
        self._last_price = price
        self._traded_volume += volume
        self._last_trades.append((timestamp, price, volume))

        self._last_timestamp = max(self._last_timestamp, timestamp)

    def reset_changes(self):
        """Clears last trades and the sets of changed level prices."""
        self._last_trades.clear()
        self._last_ask_prices.clear()
        self._last_bid_prices.clear()

    def get_snapshot(self, is_incremental=False, max_levels=10, max_trades=10):
        """Returns a immutable copy of this orderbook with levels and trades
        clipped to the given lengths.

        If is_incremental is True, only changed price-levels will be returned,
        and the param max_levels will be ignored.
        """
        if is_incremental:
            bid_levels = [
                (price, *self._bid_levels[price])
                for price in reversed(self._last_bid_prices)
            ]
            ask_levels = [
                (price, *self._ask_levels[price])
                for price in self._last_ask_prices
            ]
        else:
            bid_levels = [
                (price, *vc) for price, vc in
                reversed(self._bid_levels.items()[-max_levels:])  # reversed
            ]
            ask_levels = [
                (price, *vc) for price, vc in
                self._ask_levels.items()[:max_levels]
            ]

        return StaticOrderBook(
            symbol=self._symbol,
            timestamp=self._last_timestamp,
            last_price=self._last_price,
            deliver_price=self.deliver_price,
            traded_volume=self._traded_volume,
            bid_order_count=self._bid_order_count,
            ask_order_count=self._ask_order_count,
            bid_volume=self._bid_volume,
            ask_volume=self._ask_volume,
            bid_depth=len(self._bid_levels),
            ask_depth=len(self._ask_levels),
            bid_levels=bid_levels,
            ask_levels=ask_levels,
            last_trades=[
                trade for i, trade in enumerate(reversed(self._last_trades))
                if i < max_trades
            ]
        )
