################################################################################
# Shared constants
################################################################################


class Limits:
    """Constants for limitations."""
    MAX_PRICE_DIFF_RATIO = 0.5
    MIN_PRICE = 1.0

    MAX_ORDER_VOLUME = 10000
    MIN_ORDER_VOLUME = 1

    MAX_ACTIVE_ORDERS = 200

    @staticmethod
    def is_volume_valid(volume):
        """Returns whether the volume is within a valid range."""
        return Limits.MIN_ORDER_VOLUME <= volume <= Limits.MAX_ORDER_VOLUME

    def lowest_price(market_price):
        return max(
            Limits.MIN_PRICE,
            market_price * (1.0 - Limits.MAX_PRICE_DIFF_RATIO)
        )

    def highest_price(market_price):
        return market_price * (1.0 + Limits.MAX_PRICE_DIFF_RATIO)

    def valid_price_range(market_price):
        return (Limits.lowest_price(market_price), Limits.highest_price(market_price))

    def bounded_price(price, market_price):
        lowest, highest = Limits.valid_price_range(market_price)
        lowest += 0.01
        highest -= 0.01
        if price < lowest:
            return lowest
        elif price > highest:
            return highest
        return price

################################################################################
# Utility classes
################################################################################


class ValueWithSpeed:
    """Maintains a value as well as its rate of change."""

    def __init__(self, init_value=0):
        self.value = init_value
        self._last_value = init_value
        self._speed = 0

    @property
    def speed(self):
        """The value's rate of change."""
        return self._speed

    def update_speed(self, elapsed):
        """Recalculates value change speed by providing the elapsed time
        since the last call of this function."""
        if elapsed > 0:
            self._speed = (self.value - self._last_value) / elapsed
            self._last_value = self.value
