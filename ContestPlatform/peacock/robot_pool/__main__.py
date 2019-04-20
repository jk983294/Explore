"""Peacock Robot Pool module"""

import time
import os.path as path

from . import RobotPool

POOL = RobotPool(path.join(path.dirname(__file__), 'config.xml'))

POOL.start_server()
POOL.start()

print('Robot Pool module started.')

try:
    while True:
        time.sleep(9999)
except KeyboardInterrupt:
    POOL.stop_server()
