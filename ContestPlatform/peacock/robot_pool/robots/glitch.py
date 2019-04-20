from ..._pyprotos.common_pb2 import BID, ASK, LONG, SHORT
from ..robot import OrderParams, SharedInfoKey as SIKey
from .base_common import PriceBase

import numpy as np

_PRICESIGMA = 0.05
_BASEVOLUME = 10
_VOLUMEEXP = 1.5
_VOLUMESIGMA = 0.1
_K = 0.5
_B = 0.01
_MAXORDERS = 50


class Glitch(PriceBase):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.TargetPrice = {}
        self.price_sigma = float(xml_node.get('price_sigma', _PRICESIGMA))
        self.base_volume = int(xml_node.get('base_volume', _BASEVOLUME))
        self.volume_exp = float(xml_node.get('volume_exp', _VOLUMEEXP))
        self.volume_sigma = float(xml_node.get('volume_sigma', _VOLUMESIGMA))
        self.k = float(xml_node.get('k', _K))
        self.b = float(xml_node.get('b', _B))
        self.max_orders = int(xml_node.get('max_orders', _MAXORDERS))

    def update(self):
        if len(self.TargetPrice) < len(self.symbols):
            self.TargetPrice = {symbol: self.MarketPrice[symbol] *
                                np.exp(np.random.randn() * self.price_sigma) for symbol in self.symbols}
        else:
            fp = self.shared_info[SIKey.SYM_FP]
            self.TargetPrice = {symbol: fp[symbol] *
                                np.exp(np.random.randn() * self.price_sigma) for symbol in self.symbols}

    def generateOrders(self):
        '''
        the further the price is away from fair price, the thicker order volume is
        '''
        params = [self._generateOrder(symbol) for symbol in self.symbols]
        return params

    def _generateOrder(self, symbol, tick=0.01):
        current = self.market_client.instruments[symbol].current
        bids = [quote.price for quote in current.bid_levels]
        asks = [quote.price for quote in current.ask_levels]
        if not len(bids) or not len(asks):
            bids = [self.shared_info[SIKey.SYM_FP].get(symbol, self.MarketPrice[symbol]) - 0.01]
            asks = [self.shared_info[SIKey.SYM_FP].get(symbol, self.MarketPrice[symbol]) + 0.01]
        mid = (bids[0] + asks[0]) / 2
        tp = self.TargetPrice[symbol]
        pdist = tp - mid
        if pdist > 0:
            side = BID
            pos_type = LONG
            price = mid + self.k * pdist - self.b  # b is positive
            base = self.base_volume * np.exp(np.random.randn() * self.volume_sigma)
            volume = int(base)
            if price >= asks[0]:
                price = asks[0]
                level = (tp / price - 1) * 1e+4  # bp
                volume = int(base * self.volume_exp**level)
            param = OrderParams(side, symbol, volume, price, pos_type)
        elif pdist < 0:
            side = ASK
            pos_type = SHORT
            price = mid + self.k * pdist + self.b  # b is positive
            base = self.base_volume * np.exp(np.random.randn() * self.volume_sigma)
            volume = int(base)
            if price <= bids[0]:
                price = bids[0]
                level = (1 - tp / price) * 1e+4  # bp
                volume = int(base * self.volume_exp**level)
            param = OrderParams(side, symbol, volume, price, pos_type)
        return param
