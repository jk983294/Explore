import time

from ..robot import Robot, OrderParams

from ..._pyprotos.common_pb2 import BID, ASK, LONG
from ...common import Limits


class PriceProbe(Robot):
    """Defines a set of action methods that subclasses may implement."""

    def on_started(self):
        super().on_started()
        self.should_open = True
        self.steps = 0

    def on_step(self):
        if self.market_client.update_count < 1:
            time.sleep(0.5)
            return  # Market data unavailable (yet)

        self.steps += 1
        print('STEP', self.steps)
        side = BID if self.should_open else ASK

        for instrument in self.market_client.instruments.values():
            timestamp = instrument.current.timestamp
            market_price = instrument.current.last_price
            print('  >>> [T=%.3f] %s at %.2f' % (timestamp, instrument.symbol, market_price))

            result_code = self.order(OrderParams(
                side=side, symbol=instrument.symbol, volume=1, price=None, pos_type=LONG
            ))
            print('  ... Ordered with code', result_code)

        self.should_open = (not self.should_open)  # reverse side
