"""Implements a random investing strategy."""

import random

from ...common import Limits
from ..._pyprotos.common_pb2 import (
    BID, ASK, LONG, SHORT
)

from ..robot import OrderParams
from .base_robot import BaseRobot


class MarketNobrainer(BaseRobot):
    """Places orders randomly around current market price."""

    def on_started(self):
        super().on_started()

        # Determines the range of fair price relative to market price
        self.price_radius = abs(random.normalvariate(0, 10))

        self.order_cash_mean = random.uniform(2000, 50000)
        self.order_cash_sigma = 0.2 * self.order_cash_mean

    def decide_fair_price(self, symbol):
        """Determines the 'reasonable' price of an instrument.

        Returns a tuple (price, confidence).
        """
        instrument = self.market_client.instruments[symbol]
        market_price = instrument.current.last_price

        # Fair price is the market price plus a random offset
        offset = random.uniform(-self.price_radius, self.price_radius)

        price = market_price + round(offset) * instrument.tick

        # This "no-brainer"'s confidence is always 1.
        return Limits.bounded_price(price, market_price), 1.0

    def decide_order_price(self, side, market_price, fair_price):
        """Determines at what price to place a new order on the given side."""
        # M: market price    F: fair price
        # LOWER <-------------------M------------------> HIGHER
        # To buy:            <------M------>F
        #            <------F------>M
        # To Sell:                  M<------F------>
        #                   F<------M------>
        delta = fair_price - market_price

        if side == BID:
            if delta >= 0:
                # Price will rise, buy around market price
                price = random.uniform(market_price - delta, fair_price)
            else:
                # Price will drop, buy around fair price
                price = random.uniform(fair_price + delta, market_price)
        else:
            if delta >= 0:
                # Price will rise, sell around fair price
                price = random.uniform(market_price, fair_price + delta)
            else:
                # Price will drop, sell around market price
                price = random.uniform(fair_price, market_price - delta)

        return Limits.bounded_price(price, market_price)

    def decide_open_volume(self, price, confidence):
        """Given the order price and a price trend confidence, determines the volume
        to open a position."""
        cash = random.normalvariate(self.order_cash_mean, self.order_cash_sigma)
        if cash > self.trade_client.available_cash:
            cash = self.trade_client.available_cash

        margin_rate = self.trade_client.trader_info.margin_rate
        volume = int(cash / margin_rate / price)

        if volume < Limits.MIN_ORDER_VOLUME:
            volume = Limits.MIN_ORDER_VOLUME
        elif volume > Limits.MAX_ORDER_VOLUME:
            volume = Limits.MAX_ORDER_VOLUME

        return volume

    def decide_close_volume(self, price, avail_volume):
        cash = random.normalvariate(self.order_cash_mean, self.order_cash_sigma)

        margin_rate = self.trade_client.trader_info.margin_rate
        volume = int(cash / margin_rate / price)

        if volume < Limits.MIN_ORDER_VOLUME:
            volume = Limits.MIN_ORDER_VOLUME
        elif volume > Limits.MAX_ORDER_VOLUME:
            volume = Limits.MAX_ORDER_VOLUME

        if volume >= avail_volume:
            volume = avail_volume

        return volume

    def decide_open_order(self):
        # Choose a random instrument
        symbol = random.choice(self.market_client.symbols)
        instrument = self.market_client.instruments[symbol]

        market_price = instrument.current.last_price
        fair_price, confidence = self.decide_fair_price(symbol)

        if market_price <= fair_price:
            # Under-evaluated, should buy long
            side, pos_type = BID, LONG
        else:
            # Over-evaluated, should sell short
            side, pos_type = ASK, SHORT

        price = self.decide_order_price(side, market_price, fair_price)
        volume = self.decide_open_volume(price, confidence)

        if volume < Limits.MIN_ORDER_VOLUME:
            return None

        return OrderParams(side, symbol, volume, price, pos_type)

    def decide_close_order(self):
        pos_candidates = [
            (LONG, symbol, pos.volume)
            for symbol, pos in self.trade_client.long_positions.items()
            if pos.volume > 0
        ]
        pos_candidates.extend([
            (SHORT, symbol, pos.volume)
            for symbol, pos in self.trade_client.short_positions.items()
            if pos.volume > 0
        ])
        if not pos_candidates:
            return None

        # Choose a random position to close
        pos_type, symbol, avail_volume = random.choice(pos_candidates)

        instrument = self.market_client.instruments[symbol]
        market_price = instrument.current.last_price
        fair_price, confidence = self.decide_fair_price(symbol)

        side = BID if pos_type == SHORT else ASK

        price = self.decide_order_price(side, market_price, fair_price)
        volume = self.decide_close_volume(price, avail_volume)

        if volume < Limits.MIN_ORDER_VOLUME:
            return None

        return OrderParams(side, symbol, volume, price, pos_type)
