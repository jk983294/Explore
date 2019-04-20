from ...common import Limits
from ..._pyprotos.common_pb2 import BID, ASK, LONG, SHORT
from ..robot import Robot, OrderParams, SharedInfoKey as SIKey

import common_pb2
import broker_pb2

import numpy as np
import time
from collections import deque

_REVCOEF = 0.8
_TVR = 0.4
_TVR2BP = 10
_TVRSIGMA = 0.2
_MAXSPR = 0.8
_MINSPR = 0.0
_SPR2BP = 0.2
_SPRSIGMA = 0.0
_LEVEL = 10
_CLEARMAX = 500
_OBVMIN = 50
_OBVMAX = 100
_OBVSIGMA = 0.2
_OBVUB = 0.5
_OBVLB = 0.3
_ABV2RET = 1000
_ABVCORR = 0.8
_TICK = 0.01
_VERBOSE = 1

_sleep = 0.01


class GodDerivative(Robot):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.symbol = xml_node.get('symbol')
        self.revcoef = max(-0.99, min(0.99, float(xml_node.get('revcoef', _REVCOEF))))
        self.tvr_max = max(0, float(xml_node.get('tvr_max', _TVR)))
        self.tvr2bp = max(0, float(xml_node.get('tvr2bp', _TVR2BP)))
        self.tvrsigma = max(0, float(xml_node.get('tvrsigma', _TVRSIGMA)))
        self.maxspr = max(0, float(xml_node.get('maxspr', _MAXSPR)))
        self.minspr = max(0, float(xml_node.get('minspr', _MINSPR)))
        self.spr2bp = max(0, float(xml_node.get('spr2bp', _SPR2BP)))
        self.sprsigma = max(0, float(xml_node.get('sprsigma', _SPRSIGMA)))
        self.level = max(5, int(xml_node.get('level', _LEVEL)))
        self.clear_max = max(100, int(xml_node.get('clear_max', _CLEARMAX)))
        self.obv_min = max(1, int(xml_node.get('obv_min', _OBVMIN)))
        self.obv_max = max(1, int(xml_node.get('obv_max', _OBVMAX)))
        self.obv_sigma = max(0, float(xml_node.get('obv_sigma', _OBVSIGMA)))
        self.obv_ub = max(0, float(xml_node.get('obv_ub', _OBVUB)))
        self.obv_lb = max(0, float(xml_node.get('obv_lb', _OBVLB)))
        self.abv2ret = abs(float(xml_node.get('abv2ret', _ABV2RET)))
        self.abvcorr = max(-1, min(1, float(xml_node.get('abvcorr', _ABVCORR))))
        self.tick = max(0.01, float(xml_node.get('tick', _TICK)))
        self.verbose = int(xml_node.get('verbose', _VERBOSE))
        self.id = xml_node.get('id')
        self._cc = 0

    def on_step(self):
        if SIKey.SYM_FP not in self.shared_info or self.symbol not in self.shared_info[SIKey.SYM_FP] or len(self.shared_info[SIKey.SYM_FP][self.symbol]) < 2:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        if not self.trade_client.account.is_alive:
            # "Look, someone is cheating!!!"
            self.reborn()

        if self.id not in self.shared_info[SIKey.UPDATE]:
            self.shared_info[SIKey.UPDATE][self.id] = True

        if self.shared_info[SIKey.UPDATE][self.id]:
            self.placeOrders()
            self.shared_info[SIKey.UPDATE][self.id] = False

    def order(self, params: OrderParams, orig_timestamp=None):
        try:
            super().order(params, orig_timestamp)
        except Exception as e:
            print(e)
            print(params)

    def detail_order(self, param, orig_timestamp=None):
        response = self.trade_client._broker.new_order(broker_pb2.TraderRequest(
            trader_id=self.trade_client.trader_id, trader_pin=self.trade_client.trader_pin,
            request_type=common_pb2.NEW_ORDER, side=param.side, symbol=param.symbol,
            volume=param.volume, price=param.price or 0, is_market=(param.price is None),
            pos_type=param.pos_type, orig_timestamp=orig_timestamp or 0
        ))
        self.trade_client._handle_response(response)
        return response

    def placeOrders(self):
        # calculat new mid price
        current = self.market_client.instruments[self.symbol].current
        bids = current.bid_levels
        asks = current.ask_levels
        if self.verbose:
            print(asks)
            print(bids)
        mid = self.getMidPrice()
        next_mid = self.predictNextMidPrice()
        pavg = (mid + next_mid) / 2
        bp = abs(next_mid / mid - 1)
        tvr_max = int(self.obv_max * self.tvr_max * max(0, 1 - bp / self.tvr2bp))
        spread = min(self.maxspr, max(self.minspr, self.spr2bp * bp * np.exp(np.random.randn() * self.sprsigma)))
        init_next_ask = round(next_mid * (1 + spread), 2)
        init_next_bid = min(round(next_mid * (1 - spread), 2), init_next_ask - self.tick)
        if self.verbose:
            print('#' * 10, 'INIT', '#' * 10)
            print('CMID', mid)
            print('NMID', next_mid)
            print('BID', init_next_bid)
            print('ASK', init_next_ask)
        next_ask = init_next_ask
        next_bid = init_next_bid
        params = []

        next_mid = (next_ask + next_bid) / 2
        if self.verbose:
            print('#' * 10, 'CHANGE', '#' * 10)
            print('BID', next_bid)
            print('ASK', next_ask)

        # rebuild the distribution
        # target volume
        tvol = self.getTargetVolumeDistribution(next_ask, next_bid)
        sorted_price = sorted(list(tvol.keys()))
        max_ask = sorted_price[-1]
        min_bid = sorted_price[0]
        # current god's volume on each price level
        cvol = {}
        active_orders = self.trade_client.active_orders
        order_ids = list(active_orders.keys())
        for oid in order_ids:
            if oid not in active_orders:
                continue
            order = active_orders[oid]
            oprice = round(order.init_price, 2)
            if oprice not in cvol:
                cvol[oprice] = 0
            cvol[oprice] += order.volume
        # cancel orders out of levels and orders in levels that exceeds the target volume
        for oid in order_ids:
            if oid not in active_orders:
                continue
            order = active_orders[oid]
            oprice = round(order.init_price, 2)
            if order.init_price < next_ask and order.side == ASK:
                self.cancel(oid)
                self._cc += 1
                continue
            if order.init_price > next_bid and order.side == BID:
                self.cancel(oid)
                self._cc += 1
                continue
            if order.init_price > max_ask * 1.05 or order.init_price < min_bid * 0.95:
                self.cancel(oid)
                self._cc += 1
                continue
            if oprice in tvol and cvol.get(oprice, 0) > max(tvol[oprice] * (1 + self.obv_ub), tvol[oprice] + self.obv_max * 1):
                self.cancel(oid)

        # re-order
        for price, target_volume in tvol.items():
            price = round(price, 2)
            volume = 0
            if max(target_volume * (1 + self.obv_ub), target_volume + self.obv_max * 1) < cvol.get(price, 0):
                volume = int(target_volume * (1 + np.random.uniform(-self.obv_lb, self.obv_lb)))
            if cvol.get(price, 0) < target_volume * (1 - self.obv_lb):
                volume = int(target_volume * (1 + np.random.uniform(-self.obv_lb, self.obv_lb)) - cvol.get(price, 0))
            if price >= next_mid:
                side = ASK
                pos_type = SHORT
            elif price <= next_mid:
                side = BID
                pos_type = LONG
            if volume > 0:
                param = OrderParams(side, self.symbol, volume, round(price, 2), pos_type)
                r = self.order(param)
                if self.verbose:
                    print(param)
                params.append(param)
        time.sleep(0.01)
        if self.verbose:
            print(sorted(tvol.items(), key=lambda x: x[0]))
            self._print('REBUILD')
        # print('[%s]' % self.id, len(self.trade_client.active_orders), self._cc, self.total_cancel_count, self.total_order_count)
        return params

    def getMidPrice(self):
        current = self.market_client.instruments[self.symbol].current
        mp = current.last_price
        bids = current.bid_levels
        asks = current.ask_levels
        if len(bids):
            b1 = bids[0].price
        else:
            b1 = mp
        if len(asks):
            a1 = asks[0].price
        else:
            a1 = mp
        mid = (a1 + b1) / 2
        return round(mid, 3)

    def predictNextMidPrice(self):
        '''
        stable process-AR
        '''
        mid = self.getMidPrice()
        fp = self.shared_info[SIKey.SYM_FP][self.symbol][0]
        next_fp = self.shared_info[SIKey.SYM_FP][self.symbol][1]
        if self.verbose:
            print("FP:", fp)
            print("NFP:", next_fp)
        next_mid = next_fp + (mid - fp) * self.revcoef
        mp = self.market_client.instruments[self.symbol].current.last_price
        if next_mid > mp * 1.48:
            next_mid = mp * 1.45
        elif next_mid < mp * 0.52:
            next_mid = mp * 0.55
        next_mid = (int(next_mid * 100) + 0.5) / 100
        return next_mid

    def getTargetVolumeDistribution(self, next_ask, next_bid, n=5):
        # fp-ret of next n steps
        sfp = np.array(self.shared_info[SIKey.SYM_FP][self.symbol])
        ret_real = sfp[n:] / sfp[:-n] - 1
        ret_std = ret_real.std()
        ret = ret_real[1] * self.abvcorr + np.sqrt(1 - self.abvcorr**2) * ret_std * np.random.randn()
        # ret = ret_real

        # distribution that is proportional to ret
        # abv
        ask1_volume = max(self.obv_min, self.obv_max * min(10, np.exp(-self.abv2ret * ret)))
        bid1_volume = max(self.obv_min, self.obv_max * min(10, np.exp(self.abv2ret * ret)))
        tvol = {}
        for l in range(-self.level, self.level):
            max_ = ask1_volume
            k = round(next_ask + l * self.tick, 2)
            if l < 0:
                max_ = bid1_volume
                k = round(next_bid + (l + 1) * self.tick, 2)
            x = abs(l + 0.5)
            w = (x - 0.5) / (self.level - 1)
            v = w * self.obv_min + (1 - w) * max_
            tvol[k] = v

        return tvol

    def _print(self, title):
        print('#' * 10, title, '#' * 10)
        current = self.market_client.instruments[self.symbol].current
        if len(current.bid_levels):
            print('Bid', {'price': current.bid_levels[0].price, 'volume': current.bid_levels[0].volume})
        else:
            print('Bid', 'empty')
        print('Last price', current.last_price)
        if len(current.ask_levels):
            print('Ask', {'price': current.ask_levels[0].price, 'volume': current.ask_levels[0].volume})
        else:
            print('Ask', 'empty')
