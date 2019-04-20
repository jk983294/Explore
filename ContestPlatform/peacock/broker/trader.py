"""
Trader Account.
"""

import threading
from collections import deque, namedtuple, defaultdict
from enum import IntEnum

from .._pyprotos.common_pb2 import (
    BID, ASK, LONG, SHORT,
    ORDER_INITIAL, ORDER_ACCEPTED, ORDER_TRADED,
    ORDER_FINISHED, ORDER_CANCELLED, ORDER_REJECTED
)

from .fees import Fees


################################################################################
# Order
################################################################################

# Records a single trade transaction of an Order.
OrderTrade = namedtuple('OrderTrade', [
    'price', 'volume'
])


class Order:
    """An order in the Broker.

    An Order object keeps track of all the dynamic properties in an order's
    lifespan, including required cash, commission fee, etc.

    Call order.on_trade() method to update properties w.r.t a trade.
    """

    def __init__(self, fees, order_id, side, symbol,
                 price, volume, pos_type, market_price):
        self._order_id = order_id
        self._side = side
        self._symbol = symbol
        self._init_volume = volume
        self._init_price = price
        self._pos_type = pos_type
        self._fees = fees

        self._state = ORDER_INITIAL  # not acknowledged by Exchange yet
        self._volume = volume       # unfulfilled volume
        self._commission = 0        # commission charged so far
        self._total_money = 0       # total traded money

        self._trade_log = deque()

        self._required_cash = 0.0

        self._update_required_cash(price or market_price)

    @property
    def state(self):
        """One of OrderState constants defined in common.proto."""
        return self._state

    @state.setter
    def state(self, new_state):
        """Setter for the order state."""
        # Sanity check
        if new_state == ORDER_ACCEPTED or new_state == ORDER_REJECTED:
            assert self._state == ORDER_INITIAL, 'overwriting existing state with ACCEPTED'
            assert self._volume == self._init_volume
        elif new_state == ORDER_TRADED:
            assert self.is_active, 'inactive order cannot be traded'
            assert self._volume < self._init_volume
        elif new_state == ORDER_FINISHED:
            assert self.is_active, 'inactive order cannot be finished'
            assert self._volume == 0, 'finishing a partially filled order'
        elif new_state == ORDER_CANCELLED:
            assert self.is_active, 'inactive order cannot be cancelled'
            assert self._volume > 0, 'order already finished'
        else:
            raise ValueError('invalid order state')

        self._state = new_state

    @property
    def is_active(self):
        """Whether the order is in one of the active states."""
        return (
            self._state is ORDER_INITIAL or
            self._state == ORDER_ACCEPTED or
            self._state == ORDER_TRADED
        )

    @property
    def order_id(self):
        """ID of this order assigned by the Broker."""
        return self._order_id

    @property
    def side(self):
        """Side of thie order: BID (buy) or ASK (sell)."""
        return self._side

    @property
    def symbol(self):
        """Symbol of the order instrument."""
        return self._symbol

    @property
    def volume(self):
        """Unfilled volume remaining in this order."""
        return self._volume

    @property
    def init_volume(self):
        """Initial volume of this order."""
        return self._init_volume

    @property
    def init_price(self):
        """Price of the order, or None if this is a market order."""
        return self._init_price

    @property
    def position_type(self):
        """Type of the trader position: LONG or SHORT."""
        return self._pos_type

    @property
    def is_open(self):
        """Whether the order is opening a position."""
        if self._pos_type == LONG:
            return self._side == BID
        return self._side == ASK

    @property
    def is_close(self):
        """Whether the order is closing a position."""
        if self._pos_type == LONG:
            return self._side == ASK
        return self._side == BID

    @property
    def required_cash(self):
        """Cash needed for fulfilling the remainder of this order (open only)."""
        return self._required_cash

    @property
    def required_volume(self):
        """Volume needed for fulfilling this order (close only)."""
        return self._volume if self.is_close else 0

    @property
    def average_price(self):
        """Average trade price. 0 if no trade is fulfilled yet."""
        if self._init_volume == self._volume:
            return 0.0
        return self._total_money / (self._init_volume - self._volume)

    @property
    def commission(self):
        """Total commission charged for this order so far."""
        return self._commission

    def on_trade(self, price, volume):
        """Updates remaining volume, locked cash, and commission when a trade
        is made regarding this order.

        This function must be called by the Trader when handling ORDER_TRADED
        events.
        """
        assert price > 0
        assert 0 < volume <= self._volume
        assert self.is_active, 'trading inactive order!'

        self._volume -= volume
        self._total_money += price * volume
        self._commission += self._fees.trade_commission(price, volume)
        self._trade_log.append(OrderTrade(price, volume))

        self._update_required_cash(price)

    def __str__(self):
        state_names = (
            'INITIAL  ',
            'ACCEPTED ',
            'TRADED   ',
            'FINISHED ',
            'CANCELLED',
            'REJECTED '
        )
        side_names = ('BUY ', 'SELL')
        pos_names = ('LONG ', 'SHORT')
        # ID, state, symbol, side, pos, volume/init_volume, avg_price
        return '%-5d %s  %s  %s %s %3d/%-3d  %.2f' % (
            self.order_id, state_names[self.state], self.symbol,
            side_names[self.side], pos_names[self._pos_type],
            self.volume, self.init_volume, self._total_money)

    def _update_required_cash(self, trade_price):
        if self.is_close:
            return

        base_cash = trade_price * self._volume * self._fees.margin_rate
        commission = self._fees.trade_commission(trade_price, self._volume)

        self._required_cash = base_cash + commission


################################################################################
# The Trader Account
################################################################################

# Represents the dynamic properties of an order
OrderUpdate = namedtuple('OrderUpdate', [
    'order_id', 'symbol', 'side', 'pos_type', 'init_price', 'init_volume',
    'state', 'volume', 'avg_price', 'commission'
])

PositionUpdate = namedtuple('PositionUpdate', [
    'volume', 'locked_volume', 'occupied_cash', 'avg_price',
    'unrealized_pnl', 'realized_pnl'
])

TraderUpdate = namedtuple('TraderUpdate', [
    'is_alive', 'total_cash', 'locked_cash', 'occupied_cash',
    'unrealized_pnl', 'realized_pnl', 'commission',
    'long_positions', 'short_positions', 'orders'
])


class TraderStatus(IntEnum):
    """A Trader will enter MARGIN_CALL status if their available cash is
    below a threshold.
    A Trader in MARGIN_CALL status cannot place new orders or cancel
    existing orders. Their orders will be cancelled, and their positions
    might be forcefully closed at market price until they have enough
    available cash, at which point their status will return NORMAL.
    If a Trader does not have enough available cash, and no margin-call
    actions can be made, their status will become DISABLED permanently.
    """
    NORMAL = 0
    MARGIN_CALL = 1
    DISABLED = 2


class Trader(object):
    """Manages a trader's account, portfolio, and orders.

    The trader account can only be mutated by three methods:
        add_order: may affect orders and their dependents.
        on_order_event: may affect both orders and positions.
        on_prices_change: may affect positions and their dependents.

    The trader info will be accessed in 4 scenarios:
        1. Client requiring full info:
            (rarely) when a trader registers or logs in.

        2. Client requiring incremental info:
            (frequently) whenever a trader add/cancel an order.
            Use: get_batch_update()

        3. Client requiring partial (e.g. only orders) info:
            (not too frequently)

        4. Admin requiring summary info:
            (< once per second)

    To avoid unnecessary recomputation of "dependent variables" such as
    total locked cash, occupied cash, or unrealized PnL, Trader class
    supports a "batch mode". When enabled, calls to the above three
    methods would not immediately update the dependent variables, but
    record the positions and orders that are affected. A later call to
    get_batch_update() will then update these values, and also return
    a TraderUpdate object that summarizes the changes to the account in
    the past "batch".

    This class is *not* thread-safe.
    """

    def __init__(self, trader_id, name, pin, init_cash, fees: Fees, batch_mode=True):
        self._trader_id = trader_id
        self._name = name
        self._pin = pin

        self._status = TraderStatus.NORMAL
        self._margin_call_count = 0

        self._init_cash = init_cash
        self._total_cash = init_cash

        self._realized_pnl = 0.0
        self._commission = 0.0

        # Cache of computed variables.
        self._locked_cash = 0.0
        self._occupied_cash = 0.0
        self._unrealized_pnl = 0.0

        # Access a position by self._positions[pos_type][symbol]
        self._positions = tuple({} for _ in range(max(LONG, SHORT) + 1))

        # Active orders
        self._orders = {}  # Order ID -> Order

        # Cancelled or finished orders go here.
        self._archived_orders = deque(maxlen=1000)

        self._fees = fees

        self._lock = threading.Lock()

        # For batch updating

        self._batch_mode = batch_mode

        self._updated_orders = {}   # order_id -> order
        self._updated_positions = tuple({} for _ in range(max(LONG, SHORT) + 1))
        self.volume_stats = defaultdict(int)

    def get_update(self, incremental=False):
        """Returns a TraderUpdate that summarizes properties of this account.

        Setting `incremental` to True will return only positions/orders changed
        in the current batch, and start tracking changes in a new batch.
        """
        with self._lock:
            if incremental:
                update = self._create_update(
                    self._updated_positions, self._updated_orders
                )
                # if self.name.startswith("Team") and len(self._updated_orders) > 0:
                #     print('Incremental {}, {}'.format(len(self._updated_orders), len(update.orders)))

                # Clear caches
                self._updated_orders.clear()
                self._updated_positions[LONG].clear()
                self._updated_positions[SHORT].clear()

            else:
                update = self._create_update(self._positions, self._orders)

        return update

    def get_order_symbol(self, order_id):
        """Returns the symbol of a specified order of this Trader."""
        order = self._orders.get(order_id)
        return order.symbol if order else None

    def add_order(self, order_id, side, symbol, volume, price, market_price, pos_type):
        """Validates and adds a new order to this account.

        If the account has sufficient assets for this order, the method
        will lock the appropriate amount of assets and returns True.
        Otherwise, the method ignores the order and returns False.
        """
        if not self._batch_mode:
            raise NotImplementedError

        order = Order(
            fees=self._fees,
            order_id=order_id,
            side=side,
            symbol=symbol,
            volume=volume,
            price=price,
            pos_type=pos_type,
            market_price=market_price
        )

        with self._lock:
            if order.is_open:
                # To open a position, we need to lock some cash.
                if self.available_cash >= order.required_cash:
                    # No need to recalculate from scratch
                    self._locked_cash += order.required_cash
                else:
                    return False
            else:
                # To close a position, we need to lock some volume.
                position = self._positions[order.position_type].get(order.symbol)
                if not position or not position.lock(order.volume):
                    return False

            self._orders[order_id] = order
            self._updated_orders[order_id] = order

        return True

    def record_volume(self, symbol, volume):
        self.volume_stats[symbol] += volume
        if symbol == 'A000.PSE' or symbol == 'B000.PSE':
            pass
        else:
            self.volume_stats['all'] += volume

    def on_order_event(self, order_id, state, trade_price=None, trade_volume=None):
        """Handles an order event related to this Trader.

        Called by the Broker when an order placed by this trader has generated
        an event in the Exchange. Properties of the Position and Order objects
        will be updated, but computed properties such as total_value,
        available_cash, unrealized_pnl etc. will NOT be updated.
        """

        if not self._batch_mode:
            raise NotImplementedError

        order = self._orders.get(order_id)
        if order is None:
            raise KeyError('Trader %d: Order %d does not exist!' % (
                self._trader_id, order_id
            ))
        assert order.is_active, 'inactive order cannot be traded'

        with self._lock:
            symbol = order.symbol

            if state in (ORDER_TRADED, ORDER_FINISHED):
                # Update order's volume and required cash
                order.on_trade(trade_price, trade_volume)
                self.record_volume(symbol, trade_volume)

                # Position changes
                position = self._get_position(order.position_type, symbol)
                realized_pnl = 0
                if order.is_open:
                    position.open(trade_price, trade_volume)
                else:
                    realized_pnl = position.close(trade_price, trade_volume)

                # Deduct commission
                commission = self._fees.trade_commission(
                    trade_price, trade_volume
                )
                self._total_cash += realized_pnl - commission
                self._commission += commission
                self._realized_pnl += realized_pnl

                # Mark position for batch update
                self._updated_positions[order.position_type][symbol] = position

                # Check if the price change will affect any "dual" position
                dual_pos_type = LONG if order.position_type == SHORT else SHORT
                dual_pos = self._positions[dual_pos_type].get(symbol)
                if dual_pos and dual_pos.total_volume > 0:
                    dual_pos.on_price_change(trade_price)
                    self._updated_positions[dual_pos_type][symbol] = dual_pos

            # Update order state
            order.state = state
            if not order.is_active:
                # Release locked volume for the order before archiving it.
                # Locked cash for open orders will be updated passively.
                if order.required_volume > 0:
                    position = self._positions[order.position_type][symbol]
                    position.unlock(order.required_volume)
                self._archive_order(order)

            # Mark for batch updating
            # if self._name.startswith("Team"):
            #     print('Order {} {}'.format(order_id, str(order)))
            self._updated_orders[order_id] = order

    def on_prices_change(self, new_prices: dict):
        """Updates cached instrument prices.

        In batch mode, affected positions will be recorded. But the
        cached properties of the positions are not immediately
        recalculated.
        """
        if not self._batch_mode:
            raise NotImplementedError

        with self._lock:
            # Update and mark any affected position
            for sym, price in new_prices.items():
                for pos_type in (LONG, SHORT):
                    position = self._positions[pos_type].get(sym)
                    if position and position.total_volume > 0:
                        # Recalculate unrealized PnL and occupied cash
                        position.on_price_change(price)

                        self._updated_positions[pos_type][sym] = position

    def get_order_ids(self):
        """Returns a list of all order IDs, used by Broker._margin_call()
        to forcefully cancel unfulfilled orders.
        """
        with self._lock:
            return [order.order_id for order in self._orders.values()]

    def get_closeable_position(self):
        """Returns a non-empty position as a tuple (symbol, pos_type, volume)
        that can be closed forcefully upon a margin call, or None if no such
        position exists.
        """
        with self._lock:
            for pos_type in (SHORT, LONG):  # prefers closing SHORT first
                for symbol, pos in self._positions[pos_type].items():
                    if pos.volume > 0:
                        return (symbol, pos_type, pos.volume)

        return None

    def update_summary(self):
        """Recalculates total value, available cash, unrealized PnL, occupied
        cash, and locked cash."""
        with self._lock:
            self._unrealized_pnl = 0.0
            self._occupied_cash = 0.0

            for pos_type in (LONG, SHORT):
                for pos in self._positions[pos_type].values():
                    # Assuming each position's on_price_change() has already
                    # been called at this point.
                    self._unrealized_pnl += pos.unrealized_pnl
                    self._occupied_cash += pos.occupied_cash

            self._locked_cash = 0.0

            for order in self._orders.values():
                if order.is_active:
                    self._locked_cash += order.required_cash

    def deliver(self, deliveries):
        with self._lock:
            for item in deliveries:
                symbol = item.symbol
                price = item.price
                position = self._get_position(LONG, symbol)
                position.deliver(price)
                position = self._get_position(SHORT, symbol)
                position.deliver(price)

    @property
    def trader_id(self):
        """Trader ID."""
        return self._trader_id

    @property
    def name(self):
        """Name of the trader."""
        return self._name

    @property
    def pin(self):
        """Passcode for authentication."""
        return self._pin

    @property
    def status(self):
        """Only alive trader can perform trading."""
        return self._status

    @status.setter
    def status(self, new_status):
        """Setter of Trader's status property."""
        if new_status == TraderStatus.NORMAL:
            assert self._status == TraderStatus.MARGIN_CALL
        elif new_status == TraderStatus.MARGIN_CALL:
            assert self._status != TraderStatus.DISABLED
            if self._status == TraderStatus.NORMAL:
                # Counts the time this trader has received
                # margin calls.
                self._margin_call_count += 1

        self._status = new_status

    @property
    def is_alive(self):
        return self._status != TraderStatus.DISABLED

    @property
    def margin_call_count(self):
        """Times this trader has received margin calls."""
        return self._margin_call_count

    @property
    def value(self):
        """Total value of the portfolio."""
        return self._total_cash + self._unrealized_pnl

    @property
    def total_cash(self):
        return self._total_cash

    @property
    def available_cash(self):
        """Cash that can be used to open new position."""
        return (self._total_cash + self._unrealized_pnl -
                self._locked_cash - self._occupied_cash)

    @property
    def unrealized_pnl(self):
        return self._unrealized_pnl

    @property
    def realized_pnl(self):
        return self._realized_pnl

    @property
    def commission(self):
        return self._commission

    @property
    def locked_cash(self):
        return self._locked_cash

    @property
    def occupied_cash(self):
        return self._occupied_cash

    @property
    def active_order_count(self):
        """Number of active orders."""
        return len(self._orders)

    @property
    def commission_rate(self):
        """Commission rate applied to this trader."""
        return self._fees.commission_rate

    @property
    def margin_rate(self):
        """Minimum allowed margin rate."""
        return self._fees.margin_rate

    def _create_update(self, positions, orders):
        """Returns a TraderUpdate containing account summary and info of
        selected positions and orders.

        To get latest account summary, one should call update_summary()
        first.
        """
        pos_updates = tuple({} for _ in range(max(LONG, SHORT) + 1))
        for pos_type in (LONG, SHORT):
            for symbol, pos in positions[pos_type].items():
                pos_updates[pos_type][symbol] = PositionUpdate(
                    pos.volume, pos.locked_volume, pos.occupied_cash,
                    pos.avg_price, pos.unrealized_pnl, pos.realized_pnl
                )

        order_updates = {
            oid: OrderUpdate(
                oid, order.symbol, order.side,
                order.position_type, order.init_price,
                order.init_volume, order.state, order.volume,
                order.average_price, order.commission
            )
            for oid, order in orders.items()
        }

        return TraderUpdate(
            self.is_alive,
            self._total_cash, self._locked_cash, self._occupied_cash,
            self._unrealized_pnl, self._realized_pnl, self._commission,
            pos_updates[LONG], pos_updates[SHORT], order_updates
        )

    def _archive_order(self, order: Order):
        """Moves an active order to the archive."""
        self._archived_orders.append(order)
        del self._orders[order.order_id]

    def _get_position(self, pos_type, symbol):
        """Returns existing, or initializes a new position."""
        if symbol not in self._positions[pos_type]:
            pos = Position(pos_type, self._fees.margin_rate)
            self._positions[pos_type][symbol] = pos
            return pos

        return self._positions[pos_type][symbol]


################################################################################
# A Position in the Trader's Portfolio
################################################################################

class Position:
    """Position of a specific instrument.

    To open:
        position.open(price, volume)

    To close (two steps):
        1. Lock for a close order:
            closeable = position.lock(volume)
        2a. If the order is fulfilled:
            realized_cash = position.close(price, volume)
        2b. If the order is cancelled:
            position.unlock(volume)

    To update occupied cash and unrealized PnL explicitly for a price update:
        position.on_price_change(new_price)
    """

    def __init__(self, pos_type, margin_rate):
        self._margin_rate = margin_rate
        self._diff_factor = 1.0 if pos_type == LONG else -1.0

        # Market-independent variables:

        self._volume = 0
        self._locked_volume = 0
        self._avg_price = 0.0
        self._realized_pnl = 0.0

        # Market-dependent variables:

        self._occupied_cash = 0.0
        self._unrealized_pnl = 0.0

    @property
    def volume(self):
        """Closeable volume."""
        return self._volume

    @property
    def locked_volume(self):
        """Volume locked for a close order."""
        return self._locked_volume

    @property
    def total_volume(self):
        """Total open volume, including non-closeable."""
        return self._volume + self._locked_volume

    @property
    def occupied_cash(self):
        """Cash occupied for the current open position. Market-dependent."""
        return self._occupied_cash

    @property
    def unrealized_pnl(self):
        """Unrealied profit (positive) or loss (negative). Market-dependent."""
        return self._unrealized_pnl

    @property
    def realized_pnl(self):
        """Accumulative realized profit or loss."""
        return self._realized_pnl

    @property
    def avg_price(self):
        """Weighted average price of currently holding volumes."""
        return self._avg_price

    def open(self, price, volume):
        """Opens some new volume."""
        assert price > 0 and volume > 0

        orig_value = self._avg_price * self.total_volume
        added_value = price * volume

        self._volume += volume
        self._avg_price = (orig_value + added_value) / self.total_volume

        # Update unrealized pnl and occupied cash
        self.on_price_change(price)

    def close(self, price, volume):
        """Closes the given volume and returns realized pnl.

        The volume must first be locked.
        """
        assert price > 0
        assert 0 < volume <= self._locked_volume

        self._locked_volume -= volume

        # price_diff is always SELL_PRICE - BUY_PRICE, so for
        # SHORT positions, self._diff_factor is -1.
        price_diff = self._diff_factor * (price - self._avg_price)

        realized_pnl = price_diff * volume
        total_volume = self._volume + self._locked_volume

        self._realized_pnl += realized_pnl
        self._unrealized_pnl = price_diff * total_volume
        self._occupied_cash = price * total_volume * self._margin_rate

        return realized_pnl

    def deliver(self, price):
        total_volume = self._volume + self._locked_volume
        deliver_pnl = price * total_volume
        self._realized_pnl += deliver_pnl
        return deliver_pnl

    def lock(self, volume):
        """Tries to transfer the given amount from volume to locked_volume.

        Returns whether the transfer is successful.
        """
        if self._volume >= volume:
            self._volume -= volume
            self._locked_volume += volume
            return True
        return False

    def unlock(self, volume):
        """Tried to transfer the given amount from lock_volume to volume.

        Returns whether the transfer is successful.
        """
        if self._locked_volume >= volume:
            self._locked_volume -= volume
            self._volume += volume
            return True
        return False

    def on_price_change(self, new_price):
        """Updates unrealized pnl and occupied cash with current price."""
        # price_diff is always SELL_PRICE - BUY_PRICE, so for
        # SHORT positions, self._diff_factor is -1.
        price_diff = self._diff_factor * (new_price - self._avg_price)
        total_volume = self._volume + self._locked_volume

        self._unrealized_pnl = price_diff * total_volume
        self._occupied_cash = new_price * total_volume * self._margin_rate
