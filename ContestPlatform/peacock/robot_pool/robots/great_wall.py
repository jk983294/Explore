from ...common import Limits
from ..._pyprotos.common_pb2 import BID, ASK, LONG, SHORT
from ..robot import Robot, OrderParams, SharedInfoKey as SIKey

import time

_INITCASH = 100000000
_MAXPCT = 0.1
_VALUEPCT = 0.9
_PERIOD = 10


class GreatWall(Robot):
    def on_init(self, xml_node):
        super().on_init(xml_node)
        self.symbol = xml_node.get('symbol')
        self.init_cash = float(xml_node.get('init_cash', _INITCASH))
        self.max_pct = float(xml_node.get('max_pct', _MAXPCT))
        self.value_pct = float(xml_node.get('value_pct', _VALUEPCT))
        self.period = float(xml_node.get('period', _PERIOD))
        self.last_time = time.time()

    def isTimeToUpdate(self):
        if time.time() - self.last_time > self.period:
            self.last_time = time.time()
            return True
        else:
            return False

    def on_step(self):
        if SIKey.SYM_FP not in self.shared_info or self.symbol not in self.shared_info[SIKey.SYM_FP] or len(self.shared_info[SIKey.SYM_FP][self.symbol]) < 2:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        if not self.trade_client.account.is_alive:
            # "Look, someone is cheating!!!"
            self.reborn()

        if self.isTimeToUpdate():
            order_ids = list(self.trade_client.active_orders.keys())
            self.placeOrders()
            self.cancelOrders(order_ids)

    def cancelOrders(self, order_ids):
        for oid in order_ids:
            try:
                self.cancel(oid)
            except Exception as e:
                print(e)
                continue

    def placeOrders(self):
        symbol = self.symbol
        fp = self.shared_info[SIKey.SYM_FP][symbol][1]
        total_value = self.init_cash * self.value_pct
        total_volume = int(total_value / fp)
        # lower wall
        side = BID
        price = round(fp * (1 - self.max_pct), 2)
        volume = 0
        if symbol in self.trade_client.short_positions and self.trade_client.short_positions[symbol].volume > 0:
            volume = min(total_volume, self.trade_client.short_positions[symbol].volume)
            pos_type = SHORT
            param = OrderParams(side, symbol, volume, price, pos_type)
            self.order(param)
        if total_volume > volume:
            volume = total_volume - volume
            pos_type = LONG
            param = OrderParams(side, symbol, volume, price, pos_type)
            self.order(param)
        # higher wall
        side = ASK
        price = round(fp * (1 + self.max_pct), 2)
        volume = 0
        if symbol in self.trade_client.long_positions and self.trade_client.long_positions[symbol].volume > 0:
            volume = min(total_volume, self.trade_client.long_positions[symbol].volume)
            pos_type = LONG
            param = OrderParams(side, symbol, volume, price, pos_type)
            self.order(param)
        if total_volume > volume:
            volume = total_volume - volume
            pos_type = SHORT
            param = OrderParams(side, symbol, volume, price, pos_type)
            self.order(param)
