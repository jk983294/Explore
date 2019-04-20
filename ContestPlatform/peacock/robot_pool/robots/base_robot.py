"""Starting point of a simple Robot."""

import time
import random

from ..robot import Robot, OrderParams

from ...common import Limits


class BaseRobot(Robot):
    """Defines a set of action methods that subclasses may implement."""

    def on_started(self):
        super().on_started()
        self.safe_cash_ratio = random.uniform(0.6, 0.95)

    def decide_symbols(self):
        """Returns the symbols of the instruments of choice."""
        return random.sample(
            self.market_client.symbols,
            len(self.market_client.symbols)
        )

    def decide_to_cancel(self):
        """Returns True if the bot should cancel some orders."""
        order_count = len(self.trade_client.active_orders)

        max_order_count = Limits.MAX_ACTIVE_ORDERS * 4 / 5
        if order_count > max_order_count:
            return True

        locked_cash = self.trade_client.account.locked_cash
        locked_ratio = locked_cash / self.trade_client.account.total_cash
        max_locked_ratio = 0.2
        if locked_ratio > max_locked_ratio:
            return True

        return False

    def decide_orders_to_cancel(self):
        """Returns a list of IDs of the orders to be cancelled."""
        active_orders = self.trade_client.active_orders
        order_ids = sorted([oid for oid in active_orders.keys()])

        # Cancel the oldest order.
        return [order_ids[0]]

    def decide_to_open(self):
        """Returns True if the bot should open some position."""
        account = self.trade_client.account
        cash = account.total_cash - account.locked_cash - account.occupied_cash
        if account.unrealized_pnl < 0:
            cash += account.unrealized_pnl

        cash_ratio = cash / account.total_cash

        if cash_ratio <= self.safe_cash_ratio:
            return False    # Close

        weight = (cash_ratio - self.safe_cash_ratio) / (1.0 - self.safe_cash_ratio)

        return random.random() < weight

    def decide_open_order(self):
        """Decides parameters for an open order, or None if no valid order
        can be determined.
        """
        raise NotImplementedError

    def decide_close_order(self):
        """Decides parameters for a close order, or None if no valid order
        can be determined.
        """
        raise NotImplementedError

    def on_step(self):
        if self.reborn_needed:
            time.sleep(0.01)    # should not happen
            return

        if self.market_client.update_count < 1:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        if not self.trade_client.account.is_alive:
            # "Look, someone is cheating!!!"
            self.reborn_needed = True
            return

        # 1. To CANCEL or to NEW?
        if self.decide_to_cancel():
            for order_id in self.decide_orders_to_cancel():
                self.cancel(order_id)
            return

        # 2. To OPEN or to CLOSE?
        if self.decide_to_open():
            params = self.decide_open_order()
        else:
            params = self.decide_close_order()

        if params:
            self.order(params)
