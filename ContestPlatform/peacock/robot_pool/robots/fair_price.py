'''A robot that determines fair price according to model'''

from ..robot import Robot, SharedInfoKey as SIKey
from . import stock
from . import derivative

import numpy as np
from collections import deque
import time
import pprint

_PERIOD = 10
_PERIODSIGMA = 0
_FORWARDSTEP = 5
_MAXLEN = 2000
_INITSIGMA = 0.0005


class FairPrice(Robot):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.symbols = self.market_client.symbols
        self.period = float(xml_node.get('period', _PERIOD))
        self.period_sigma = int(xml_node.get('period_sigma', _PERIODSIGMA))
        self.forward_step = int(xml_node.get('forward_step', _FORWARDSTEP))
        self.history_maxlen = int(xml_node.get('history_maxlen', _MAXLEN))
        self.history = {symbol: deque(maxlen=self.history_maxlen) for symbol in self.symbols}
        self.init_sigma = float(xml_node.get('init_sigma', _INITSIGMA))
        node = xml_node.find('stockmodel')
        stockmodelname = node.get('name')
        self.stockmodel = getattr(stock, stockmodelname)(node)
        # TODO: add derivative model
        self.derivativemodel = []
        for node in xml_node.findall('derivativemodel'):
            dmodelname = node.get('name')
            self.derivativemodel.append(getattr(derivative, dmodelname)(self.market_client, node))
        self.last_timestamp = time.time()

    def isTimeToUpdate(self):
        self.shared_info[SIKey.TIME_ELAPSE] = time.time() - self.last_timestamp
        if self.shared_info[SIKey.TIME_ELAPSE] > self.period:
            self.last_timestamp = time.time()
            self.period *= np.exp(np.random.randn() * self.period_sigma)
            self.shared_info[SIKey.PERIOD] = self.period
            return True
        else:
            return False

    def update(self):
        instruments = self.market_client.instruments
        # update stock fair price
        predict_prices = self.stockmodel.predict(self.history)
        for symbol, price in predict_prices.items():
            self.shared_info[SIKey.SYM_FP][symbol].append(price)
            self.history[symbol].append(price)
        # TODO: update derivative fair price
        for dmodel in self.derivativemodel:
            symbol = dmodel.symbol
            price = dmodel.predict(self.history)
            self.shared_info[SIKey.SYM_FP][symbol].append(price)
            self.history[symbol].append(price)
        # set update flag
        for key in self.shared_info[SIKey.UPDATE].keys():
            self.shared_info[SIKey.UPDATE][key] = True

    def on_step(self):
        '''
        update fair price
        '''
        instruments = self.market_client.instruments

        if SIKey.SYM_FP not in self.shared_info:
            # write symbol-price dict into shared_info
            if self.market_client.update_count < 1:
                return  # market data unavailable yet

            # initialize
            self.shared_info[SIKey.SYM_FP] = {}
            for symbol in self.symbols:
                price = instruments[symbol].current.last_price
                ret = 1 + np.random.randn(self.history_maxlen) * self.init_sigma
                cumret = ret.cumprod()
                cumret /= cumret[-1]
                history = [price * cumret[i] for i in range(self.history_maxlen)]
                self.history[symbol].extend(history)
                self.shared_info[SIKey.SYM_FP][symbol] = deque(maxlen=self.forward_step)
                self.shared_info[SIKey.SYM_FP][symbol].append(price)

            self.shared_info[SIKey.TIME_ELAPSE] = 0
            self.shared_info[SIKey.PERIOD] = self.period
            self.shared_info[SIKey.UPDATE] = {}

            # update self.forward_step - 1 times
            for _ in range(self.forward_step - 1):
                self.update()

        # update fair price
        if self.isTimeToUpdate():
            self.update()
            # pprint.pprint(self.shared_info)
