from . import alphaman as AlphaMan
from . import betaman as BetaMan

from collections import deque
import numpy as np

_LOOKBACK = 20
_CSVOLATILITY = 0.0005
_TSVOLATILITY = 0.0001
_CORR = 0.5
_VOLATILITYPERIOD = 20


class Meta:
    def __init__(self, xml_node):
        self._symbols = sorted(xml_node.get('symbols').split(' '))
        # load alpha
        self.Alphas = []
        for node in xml_node.findall('alpha'):
            name = node.get('name')
            self.Alphas.append(getattr(AlphaMan, name)(self._symbols, node))
        # load beta
        self.Betas = []
        for node in xml_node.findall('beta'):
            name = node.get('name')
            self.Betas.append(getattr(BetaMan, name)(self._symbols, node))
        # signal history
        self.lookback = int(xml_node.get('lookback', _LOOKBACK))
        self.cs_volatility = float(xml_node.get('cs_volatility', _CSVOLATILITY))
        self.ts_volatility = float(xml_node.get('ts_volatility', _TSVOLATILITY))
        self.corr = min(0.99, max(-0.99, float(xml_node.get('corr', _CORR))))
        self.volatility_period = int(xml_node.get('volatility_period', _VOLATILITYPERIOD))
        self.current_cs_volatility = self.cs_volatility
        self.current_ts_volatility = self.ts_volatility
        self.count_cs = 0
        self.count_ts = 0
        self.Signals = deque(maxlen=self.lookback)

    @staticmethod
    def normalize(data):
        data = np.array(data)
        mean = data.mean()
        std = data.std()
        return (data - mean) / (std + 1e-5)

    def predict(self, fp):
        '''
        fp is (symbol, deque_fp) dict
        return (symbol, fp) dict
        '''
        # alpha return
        aret = np.zeros(len(self._symbols))
        # print('Alpha:')
        for alpha in self.Alphas:
            a = alpha.predict(fp)
            # print(alpha.name, a, '%.4f' % alpha.weight)
            aret += a * alpha.weight
        aret = self.normalize(aret) * self.CrossSectionVolatility(fp)
        # beta return
        bret = 0
        # print('Beta:')
        for beta in self.Betas:
            b = beta.predict(fp)
            # print(beta.name, b, '%.4f' % beta.weight)
            bret += b * beta.weight
        self.Signals.append(bret)
        bret = self.normalize(self.Signals)[-1] * self.TimeSeriesVolatility(fp)
        # noise
        sfp = np.array([fp[symbol] for symbol in self._symbols]).T
        ret_stock = sfp[1:] / sfp[:-1] - 1
        ret_std = ret_stock.std(0)
        noise_sigma = ret_std * np.sqrt(1 - self.corr**2)
        noise = np.random.randn(len(self._symbols)) * noise_sigma
        next_fp = {}
        ret = (aret + bret) * self.corr + noise
        # print(aret + bret, self.corr, noise_sigma, noise, ret)
        for i, symbol in enumerate(self._symbols):
            next_fp[symbol] = (1 + ret[i]) * fp[symbol][-1]
        # print('Predicted fair price:')
        # for symbol in self._symbols:
            # print(symbol, next_fp[symbol])
        return next_fp

    def CrossSectionVolatility(self, fp):
        if self.count_cs == 0:
            self.current_cs_volatility = self.cs_volatility * abs(np.random.randn())
        self.count_cs += 1
        self.count_cs %= self.volatility_period
        # print('[CSVOL]', self.current_cs_volatility)
        return self.current_cs_volatility

    def TimeSeriesVolatility(self, fp):
        if self.count_ts == 0:
            self.current_ts_volatility = self.ts_volatility * abs(np.random.randn())
        self.count_ts += 1
        self.count_ts %= self.volatility_period
        # print('[TSVOL]', self.current_ts_volatility)
        return self.current_ts_volatility
