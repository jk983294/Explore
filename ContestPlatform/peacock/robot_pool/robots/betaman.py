import numpy as np
from collections import deque


class BetaBase:
    def __init__(self, symbols, xml_node):
        self._symbols = symbols
        self.weight = float(xml_node.get('weight'))
        self.name = xml_node.get('name')
        self.delay = int(xml_node.get('delay', 0))
        self.lookback = int(xml_node.get('lookback'))
        self.constants = [int(c) for c in xml_node.get('constants', '1').split(' ')]
        self.Signals = deque(maxlen=self.lookback)

    @staticmethod
    def op(data):
        '''
        normalize
        '''
        m = data.mean()
        s = data.std()
        return (data[-1] - m) / (s + 1e-5)

    def predict(self, fp):
        '''
        fp is (symbol, deque) dict
        return np.array of len=len(self._symbols)
        '''
        fp = {symbol: np.array(fp[symbol])[:-1 - self.delay] for symbol in self._symbols}
        signal = self.signal(fp)
        self.Signals.append(signal)
        signal = self.op(np.array(self.Signals))
        return signal

    def signal(self, fp):
        pass

# ret(fp, c1)


class Beta1(BetaBase, object):
    def signal(self, fp):
        signal = 0
        for symbol in self._symbols:
            signal += fp[symbol][-1] / fp[symbol][-1 - self.constants[0]] - 1
        return signal

# corrseq(ret(fp, c1), c2)


class Beta2(BetaBase, object):
    def signal(self, fp):
        signal = 0
        n = 0
        for symbol in self._symbols:
            sfp = fp[symbol]
            ret = sfp[self.constants[0]:] / sfp[:-self.constants[0]] - 1
            corr = np.corrcoef(ret[-self.constants[1]:], np.arange(self.constants[1]))[0, 1]
            if not np.isnan(corr):
                signal += corr
                n += 1
        signal /= (n + 1e-5)
        return signal

# mean(cs-std(ret(fp, c1)), c2)


class Beta3(BetaBase, object):
    def signal(self, fp):
        ret = []
        for symbol in self._symbols:
            sfp = fp[symbol]
            lret = sfp[self.constants[0]:] / sfp[:-self.constants[0]] - 1
            ret.append(lret[-self.constants[1]:])
        ret = np.array(ret)
        cs_std = ret.std(0)
        signal = cs_std.mean()
        return signal

# ts-std(rfp, c1)


class Beta4(BetaBase, object):
    def signal(self, fp):
        signal = 0
        for symbol in self._symbols:
            sfp = fp[symbol]
            ret = sfp[1:] / sfp[:-1] - 1
            signal += ret[-self.constants[0]:].std()
        return signal

# MA


class Beta5(BetaBase, object):
    def __init__(self, symbols, xml_node):
        super().__init__(symbols, xml_node)
        self.corr = float(xml_node.get('corr'))
        self.noise = deque(maxlen=2)
        self.noise.append(np.random.randn())

    @staticmethod
    def op(data):
        return data[-1]

    def signal(self, fp):
        self.noise.append(np.random.randn())
        signal = self.noise[-2] * self.corr + np.sqrt(1 - self.corr**2) * self.noise[-1]
        return signal
