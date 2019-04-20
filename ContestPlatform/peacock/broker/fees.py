"""Calculates commission and other fees for a given order."""


class Fees:
    """Fee-related constants and helper functions."""

    def __init__(self, commission_rate=0.0, margin_rate=1.0):
        self._commission_rate = commission_rate
        self._margin_rate = margin_rate

    @property
    def margin_rate(self):
        """margin rate."""
        return self._margin_rate

    @property
    def commission_rate(self):
        """Commission rate."""
        return self._commission_rate

    def trade_commission(self, price, volume):
        """Returns the commission fee for a given trade."""
        # May apply minimum fee or order-type-dependent ratio here.
        return (price * volume) * self._commission_rate
