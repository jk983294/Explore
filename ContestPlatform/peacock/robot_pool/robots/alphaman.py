import numpy as np


class AlphaBase:
    def __init__(self, symbols, xml_node):
        self._symbols = symbols
        self.weight = float(xml_node.get('weight'))
        self.name = xml_node.get('name')
        self.delay = int(xml_node.get('delay', 0))
        self.constants = [int(c) for c in xml_node.get('constants').split(' ')]

    @staticmethod
    def op(data):
        '''
        neutral and scale
        '''
        data = data - data.mean()
        data /= (np.sum(np.abs(data)) + 1e-5)
        return data

    def predict(self, fp):
        '''
        fp is (symbol, deque) dict
        return np.array of len=len(self._symbols)
        '''
        fp = {symbol: np.array(fp[symbol])[: len(fp[symbol]) - self.delay] for symbol in self._symbols}
        alpha = self.op(self.alpha(fp))
        return alpha

    def alpha(self, fp):
        pass

# ret(fp, c1)


class Alpha1(AlphaBase, object):
    def alpha(self, fp):
        '''
        fp is (symbol, ndarray) dict
        return np.array of len=len(self._symbols)
        '''
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            alpha[i] = fp[symbol][-1] / fp[symbol][-1 - self.constants[0]] - 1
        return alpha

# corr(ret(fp, c1), delay(ret(fp, c1), c2), c3)


class Alpha2(AlphaBase, object):
    def alpha(self, fp):
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            sfp = fp[symbol]
            ret = sfp[self.constants[0]:] / sfp[: -self.constants[0]] - 1
            ret1 = ret[-self.constants[2]:]
            ret2 = ret[-self.constants[1] - self.constants[2]: -self.constants[1]]
            alpha[i] = np.corrcoef(ret1, ret2)[0, 1]
            if np.isnan(alpha[i]):
                alpha[i] = 0
        return alpha

# corr(ret(fp, c1), mret(fp, c1), c2)


class Alpha3(AlphaBase, object):
    def alpha(self, fp):
        ret = []
        for symbol in self._symbols:
            sfp = fp[symbol]
            ret.append(sfp[self.constants[0]:] / sfp[: -self.constants[0]] - 1)
        ret = np.array(ret)
        mret = ret.mean(0)
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            alpha[i] = np.corrcoef(ret[i, -self.constants[1]:], mret[-self.constants[1]:])[0, 1]
            if np.isnan(alpha[i]):
                alpha[i] = 0
        return alpha

# std(diffm(ret(fp, c1)), c2)


class Alpha4(AlphaBase, object):
    def alpha(self, fp):
        ret = []
        for symbol in self._symbols:
            sfp = fp[symbol]
            ret.append(sfp[self.constants[0]:] / sfp[: -self.constants[0]] - 1)
        ret = np.array(ret)
        mret = ret.mean(0)
        ret = ret - mret[None, :]
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            alpha[i] = np.std(ret[i, -self.constants[1]:])
        return alpha

# corr(abs(diff(fp, c1)), fp, c2)


class Alpha5(AlphaBase, object):
    def alpha(self, fp):
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            sfp = fp[symbol]
            body = np.abs(sfp[: -self.constants[0]] - sfp[self.constants[0]:])
            body = body[-self.constants[1]:]
            close = sfp[-self.constants[1]:]
            alpha[i] = np.corrcoef(body, close)[0, 1]
            if np.isnan(alpha[i]):
                alpha[i] = 0
        return alpha

# sub(fp, mean(fp, c1))


class Alpha6(AlphaBase, object):
    def alpha(self, fp):
        alpha = np.empty(len(self._symbols))
        for i, symbol in enumerate(self._symbols):
            sfp = fp[symbol]
            alpha[i] = sfp[-1] / sfp[-self.constants[0]:].mean()
            if np.isnan(alpha[i]):
                alpha[i] = 0
        return alpha
