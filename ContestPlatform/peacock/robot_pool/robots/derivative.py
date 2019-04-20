import numpy as np
import math
from collections import deque


class Futures():
    def __init__(self, market_client, xml_node):
        self.underlier = xml_node.get('underlier')
        self.symbol = xml_node.get('symbol')
        self.settlement_interval = int(xml_node.get('settlement_interval'))
        self.settlement_period = int(xml_node.get('settlement_period'))
        self.verbose = int(xml_node.get('verbose'))
        self.market_client = market_client

    def predict(self, fp):
        sfp = np.array(fp[self.underlier])
        current = self.market_client.instruments[self.symbol].current
        ts = current.timestamp
        deliver_p = current.deliver_price
        time_to_maturity = self.settlement_interval - ts % self.settlement_interval
        if time_to_maturity == self.settlement_interval and ts > 1:
            time_to_maturity = 0
        if self.verbose:
            print(self.symbol, "deliver price", current.deliver_price)
        if time_to_maturity >= self.settlement_period:
            if self.verbose:
                print(self.symbol, "time to maturity", time_to_maturity, "fair price",
                      sfp[-1], "underlier fp", sfp[-1], "underlier lp", current.last_price)
            return sfp[-1]
        tmp_fp = (deliver_p * (self.settlement_period - time_to_maturity) +
                  sfp[-1] * time_to_maturity) / self.settlement_period
        print(self.symbol, "time to maturity", time_to_maturity, "fair price",
              tmp_fp, "underlier fp", sfp[-1], "underlier lp", current.last_price)
        return tmp_fp


class Square():
    def __init__(self, market_client, xml_node):
        self.underlier = xml_node.get('underlier')
        self.symbol = xml_node.get('symbol')
        self.settlement_interval = int(xml_node.get('settlement_interval'))
        self.settlement_period = int(xml_node.get('settlement_period'))
        self.verbose = int(xml_node.get('verbose'))
        self.market_client = market_client

    def predict(self, fp):
        sfp = np.array(fp[self.underlier])
        current = self.market_client.instruments[self.symbol].current
        ts = current.timestamp
        deliver_p = current.deliver_price
        ret_under = sfp[1:] / sfp[:-1] - 1
        ret_under_std = ret_under.std()
        time_to_maturity = self.settlement_interval - ts % self.settlement_interval
        if time_to_maturity == self.settlement_interval and ts > 1:
            time_to_maturity = 0
        tmp_fp = sfp[-1] * sfp[-1] * math.exp((ret_under_std ** 2) * time_to_maturity) / 100
        if self.verbose:
            print(self.symbol, "deliver price", current.deliver_price)
        if time_to_maturity >= self.settlement_period:
            if self.verbose:
                print(self.symbol, "time to maturity", time_to_maturity, "fair price", tmp_fp, "underlier fp", sfp[-1])
            return tmp_fp
        tmp_fp2 = (deliver_p * (self.settlement_period - time_to_maturity) +
                   tmp_fp * time_to_maturity) / self.settlement_period
        if self.verbose:
            print(self.symbol, "time to maturity", time_to_maturity, "fair price", tmp_fp2, "underlier fp", sfp[-1])
        return tmp_fp2


class SquareRoot():
    def __init__(self, market_client, xml_node):
        self.underlier = xml_node.get('underlier')
        self.symbol = xml_node.get('symbol')
        self.settlement_interval = int(xml_node.get('settlement_interval'))
        self.settlement_period = int(xml_node.get('settlement_period'))
        self.verbose = int(xml_node.get('verbose'))
        self.market_client = market_client

    def predict(self, fp):
        sfp = np.array(fp[self.underlier])
        current = self.market_client.instruments[self.symbol].current
        ts = current.timestamp
        deliver_p = current.deliver_price
        ret_under = sfp[1:] / sfp[:-1] - 1
        ret_under_std = ret_under.std()
        time_to_maturity = self.settlement_interval - ts % self.settlement_interval
        if self.verbose:
            print(self.symbol, "deliver price", current.deliver_price)
        if time_to_maturity == self.settlement_interval and ts > 1:
            time_to_maturity = 0
        tmp_fp = sfp[-1] ** 0.5 * math.exp(-0.125 * (ret_under_std ** 2) * time_to_maturity) * 10
        if time_to_maturity >= self.settlement_period:
            if self.verbose:
                print(self.symbol, "time to maturity", time_to_maturity, "fair price", tmp_fp, "underlier fp", sfp[-1])
            return tmp_fp
        tmp_fp2 = (deliver_p * (self.settlement_period - time_to_maturity) +
                   tmp_fp * time_to_maturity) / self.settlement_period
        if self.verbose:
            print(self.symbol, "time to maturity", time_to_maturity, "fair price", tmp_fp2, "underlier fp", sfp[-1])
        return tmp_fp2


'''
class Delay:
    def __init__(self, xml_node):
        self.underlier = xml_node.get('underlier')
        self.symbol = xml_node.get('symbol')
        self.delay = int(xml_node.get('delay'))
        self.corr = max(-1, min(1, float(xml_node.get('corr'))))

    def predict(self, fp):
        sfp = np.array(fp[self.underlier])
        ret_under = sfp[1:] / sfp[:-1] - 1
        ret_under_std = ret_under.std()
        noise_sigma = np.sqrt(1 - self.corr**2) * ret_under_std
        noise = np.random.randn() * noise_sigma
        ret = ret_under[-1 - self.delay] * self.corr + noise
        fair_price = fp[self.symbol][-1] * (1 + ret)
        return fair_price

class Hedge:
    def __init__(self, xml_node):
        self.underlier = xml_node.get('underlier')
        self.symbol = xml_node.get('symbol')
        self.delay = int(xml_node.get('delay'))
        self.corr = max(-0.99, min(0.99, float(xml_node.get('corr'))))
        self.maxlen = int(xml_node.get('maxlen'))
        self.arcoef = float(xml_node.get('arcoef'))
        self.last_random = deque([np.random.randn() * 0.001 for _ in range(self.maxlen)], maxlen=self.maxlen)

    def predict(self, fp):
        sfp = np.array(fp[self.underlier])
        ret_under = sfp[1:] / sfp[:-1] - 1
        ret_under_std = ret_under.std()
        noise_sigma = np.sqrt((1 - self.corr**2) * (1 - self.arcoef**2)) * ret_under_std
        ar_sigma = np.sqrt(1 - self.corr**2) * ret_under_std
        res_ret = self.arcoef * self.last_random[self.maxlen - self.delay] + np.random.randn() * noise_sigma
        # print(self.arcoef, self.last_random, ar_sigma, res_ret)
        self.last_random.append(res_ret)
        ret = ret_under[-1] * self.corr + res_ret
        fair_price = fp[self.symbol][-1] * (1 + ret)
        return fair_price
'''
