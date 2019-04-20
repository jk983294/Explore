"""Peacock Market Data Module"""

import time

from . import MarketData

MARKET_DATA = MarketData()

MARKET_DATA.start_server()

print('Market Data module started.')

try:
    while True:
        time.sleep(9999)
except KeyboardInterrupt:
    MARKET_DATA.stop_server()
