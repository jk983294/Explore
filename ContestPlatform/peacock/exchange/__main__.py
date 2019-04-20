"""
Peacock Exchange Module
"""

import time

from . import Exchange


EXCHANGE = Exchange()

EXCHANGE.start_server()

print('Exchange module started.')

try:
    while True:
        time.sleep(9999)
except KeyboardInterrupt:
    EXCHANGE.stop_server()
