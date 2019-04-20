from ...common import Limits
from ..._pyprotos.common_pb2 import BID, ASK, LONG, SHORT
from ..robot import Robot, OrderParams, SharedInfoKey as SIKey

import numpy as np
import time
from collections import deque

_INITCASH = 1e+8
_STRENGTH = 0.4
_SAFECASHRATIO = 0.4
_PERIOD = 10

_ORDEREXP = 2
_ORDERLEVEL = 10
_ORDERSIGMA = 0.01
_TIMEEXP = 1

_PRICESIGMA = 0.0005
_VOLUMESIGMA = 0.2
_MULTISIGMA = 1

_LOOKBACK = 10


class Base(Robot):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.symbols = self.market_client.symbols
        self.init_cash = int(xml_node.get('init_cash', _INITCASH))
        self.strength = float(xml_node.get('strength', _STRENGTH))
        self.safe_cash_ratio = float(xml_node.get('safe_cash_ratio', _SAFECASHRATIO))

        self.order_exp = float(xml_node.get('order_exp', _ORDEREXP))
        self.order_level = int(xml_node.get('order_level', _ORDERLEVEL))
        self.order_sigma = float(xml_node.get('order_sigma', _ORDERSIGMA))
        self.time_exp = float(xml_node.get('time_exp', _TIMEEXP))

    @property
    def LongPositions(self):
        pos = {}
        for symbol in self.symbols:
            if symbol not in self.trade_client.long_positions:
                pos[symbol] = 0
            else:
                pos[symbol] = self.trade_client.long_positions[symbol].volume
        return pos

    @property
    def ShortPositions(self):
        pos = {}
        for symbol in self.symbols:
            if symbol not in self.trade_client.short_positions:
                pos[symbol] = 0
            else:
                pos[symbol] = self.trade_client.short_positions[symbol].volume
        return pos

    @property
    def NetPositions(self):
        netpos = {}
        for symbol in self.symbols:
            netpos[symbol] = self.LongPositions[symbol] - self.ShortPositions[symbol]
        return netpos

    @property
    def MarketPrice(self):
        return {symbol: instrument.current.last_price for symbol, instrument in self.market_client.instruments.items()}

    @property
    def TimeRatio(self):
        w = self.shared_info.get(SIKey.TIME_ELAPSE, 0) % self.shared_info.get(SIKey.PERIOD, _PERIOD)
        w = (w / self.shared_info.get(SIKey.PERIOD, _PERIOD))**self.time_exp
        return w

    def _order_target_volume(self, symbol, volume, n, width, ratio):
        mprice = self.MarketPrice[symbol]
        trade_volume = volume - self.NetPositions[symbol]
        params = []
        if trade_volume > 0:
            side = BID
            prices = [np.random.uniform(mprice - (i + 0.5) * width, mprice - (i - 0.5) * width) for i in range(n)]
            volumes = [int(abs(trade_volume) * ratio(i)) for i in range(n)]
            combo = zip(prices, volumes)
            # close short, then open long
            short_pos = self.ShortPositions[symbol]
            for p, v in combo:
                if short_pos > 0:
                    v = min(short_pos, v)
                    short_pos -= v
                    pos_type = SHORT
                else:
                    pos_type = LONG
                if v > 0:
                    params.append(OrderParams(side, symbol, v, p, pos_type))
        elif trade_volume < 0:
            side = ASK
            prices = [np.random.uniform(mprice + (i - 0.5) * width, mprice + (i + 0.5) * width) for i in range(n)]
            volumes = [int(abs(trade_volume) * ratio(i)) for i in range(n)]
            combo = zip(prices, volumes)
            # close long, then open short
            long_pos = self.LongPositions[symbol]
            for p, v in combo:
                if long_pos > 0:
                    v = min(long_pos, v)
                    long_pos -= v
                    pos_type = LONG
                else:
                    pos_type = SHORT
                if v > 0:
                    params.append(OrderParams(side, symbol, v, p, pos_type))
        return params

    def placeOrders(self):
        self.cancelOrders()
        for param in self.generateOrders():
            self.order(param)

    def cancelAllOrders(self):
        orders = list(self.trade_client.active_orders.keys())
        for order_id in orders:
            self.cancel(order_id)

    def cancelOrders(self):
        orders = sorted(list(self.trade_client.active_orders.keys()), reverse=True)
        n = len(orders)
        while n > self.max_orders:
            print(self.name, n, 'canceling orders')
            order_id = orders.pop()
            self.cancel(order_id)
            n = len(orders)

    def update(self):
        """
        update specific fair price
        """
        pass

    def generateOrders(self):
        """
        generate OrderParams according to fair price
        """
        pass


class PriceBase(Base):
    def on_step(self):
        if self.market_client.update_count < 1:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        if not self.trade_client.account.is_alive:
            # "Look, someone is cheating!!!"
            self.reborn()

        self.update()
        self.placeOrders()


class VolumeBase(Base):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.period = int(xml_node.get('period', _PERIOD))
        self.volume_sigma = float(xml_node.get('volume_sigma', _VOLUMESIGMA))
        self.multi_sigma = float(xml_node.get('multi_sigma', _MULTISIGMA))
        self.TargetValue = {symbol: 0 for symbol in self.symbols}
        self.TargetVolume = {symbol: 0 for symbol in self.symbols}
        self.last_timestamp = time.time()

    def on_step(self):
        if self.market_client.update_count < 1:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        if not self.trade_client.account.is_alive:
            # "Look, someone is cheating!!!"
            self.reborn()

        if self.isTimeToUpdate():
            self.update()

        self.placeOrders()

    def placeOrders(self):
        self.cancelAllOrders()
        for param in self.generateOrders():
            self.order(param)

    def isTimeToUpdate(self):
        time_elapse = time.time() - self.last_timestamp
        if time_elapse > self.period:
            self.last_timestamp = time.time()
            return True
        else:
            return False

    def getRandomMultiplier(self):
        return 1 + np.random.randn() * self.multi_sigma

    def printStat(self):
        n = 10
        header = [
            ('%s', 'symbol'),
            ('%.4f', 'elapse'),
            ('%d', 'period'),
            ('%d', 't_value'),
            ('%d', 't_volume'),
            ('%d', 'long'),
            ('%d', 'short'),
            ('%d', 'net'),
            ('%d', 'trade'),
            ('%d', 'bid_long'),
            ('%d', 'bid_short'),
            ('%d', 'ask_long'),
            ('%d', 'ask_short'),
            ('%.2f', 'mktprice'),
        ]
        lines = ['#' * 20 + self.name + '#' * 20, ''.join([h + ' ' * (n - len(h)) for fmt, h in header])]
        for symbol in self.symbols:
            stat = self.getStat(symbol)
            content = [fmt % stat[h] for fmt, h in header]
            lines.append(''.join(c + ' ' * (n - len(c)) for c in content))
        lines.append('\n')
        print('\n'.join(lines))

    def getStat(self, symbol):
        stat = {
            'symbol': symbol,
            'elapse': time.time() - self.last_timestamp,
            'period': self.period,
            't_value': self.TargetValue[symbol] * 1e-4,
            't_volume': self.TargetVolume[symbol],
            'long': self.LongPositions[symbol],
            'short': self.ShortPositions[symbol],
            'net': self.NetPositions[symbol],
            'trade': self.TargetVolume[symbol] - self.NetPositions[symbol],
            'bid_long': self.OpenOrderVolume(symbol, BID, LONG),
            'bid_short': self.OpenOrderVolume(symbol, BID, SHORT),
            'ask_long': self.OpenOrderVolume(symbol, ASK, LONG),
            'ask_short': self.OpenOrderVolume(symbol, ASK, SHORT),
            'mktprice': self.MarketPrice[symbol],
        }
        return stat


class AlphaBase(VolumeBase):
    @staticmethod
    def op(alpha):
        """
        neutral and scale
        """
        symbol, array = zip(*alpha.items())
        array = np.array(array)
        array = array - array.mean()
        array /= (np.sum(np.abs(array)) + 1e-5)
        return dict(zip(symbol, array))

    def update(self):
        alphas = self.op(self.alpha())
        multiplier = self.getRandomMultiplier()
        for symbol, alpha in alphas.items():
            mp = self.MarketPrice[symbol]
            self.TargetValue[symbol] = alpha * self.strength * self.init_cash * multiplier
            self.TargetVolume[symbol] = int(self.TargetValue[symbol] / mp)

    def generateOrders(self):
        n = self.order_level
        w = self.TimeRatio
        vper = [np.exp(np.random.randn() * self.volume_sigma) for i in range(n)]
        vsum = sum(vper)
        vper = [v / vsum for v in vper]

        def ratio(i): return vper[i]
        params = []
        for symbol in self.symbols:
            volume = (1 - w) * self.TargetVolume[symbol] + w * self.NetPositions[symbol]
            mp = self.MarketPrice[symbol]
            width = mp * self.order_sigma / n
            params.extend(self._order_target_volume(symbol, volume, n, width, ratio))
        return params

    def placeOrders(self):
        self.cancelAllOrders()
        for param in self.generateOrders():
            self.order(param)

    def alpha(self):
        """
        return (symbol, alpha) dict
        """
        pass


class BetaBase(VolumeBase):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.lookback = int(xml_node.get('lookback', _LOOKBACK))
        self.Signals = deque(maxlen=self.lookback)

    @staticmethod
    def op(beta):
        """
        normalize and truncate
        """
        s = np.array(beta)
        ms = s.mean()
        ss = s.std()
        ns = 0
        if ss > 1e-5:
            ns = (s[-1] - ms) / ss
        return min(1, max(-1, ns))

    def update(self):
        signal = self.signal()
        self.Signals.append(signal)
        signal = self.op(self.Signals)
        multiplier = self.getRandomMultiplier()
        value = signal * self.strength * self.init_cash * multiplier / len(self.symbols)
        self.TargetValue = {symbol: value for symbol in self.symbols}
        self.TargetVolume = {symbol: int(value / self.MarketPrice[symbol]) for symbol, value in self.TargetValue.items()}

    def generateOrders(self):
        n = self.order_level
        w = self.TimeRatio
        vper = [np.exp(np.random.randn() * self.volume_sigma) for i in range(n)]
        vsum = sum(vper)
        vper = [v / vsum for v in vper]

        def ratio(i): return vper[i]
        params = []
        for symbol in self.symbols:
            volume = (1 - w) * self.TargetVolume[symbol] + w * self.NetPositions[symbol]
            mp = self.MarketPrice[symbol]
            width = mp * self.order_sigma / n
            params.extend(self._order_target_volume(symbol, volume, n, width, ratio))
        return params

    def signal(self):
        """
        return a single signal value
        """
        pass
