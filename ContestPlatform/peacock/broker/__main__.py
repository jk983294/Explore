"""Peacock Broker Module"""

import time
from . import Broker
import sys


def main():
    """Main entry point."""
    broker_port_base = 52500
    broker_index = 11
    exchange_port = 51701

    if len(sys.argv) < 4:
        pass
    else:
        broker_port_base = int(sys.argv[1])
        broker_index = int(sys.argv[2])
        exchange_port = int(sys.argv[3])

    broker_port = broker_port_base + broker_index
    broker_name = 'pb%d' % broker_index
    exchange_endpoint = '[::]:%d' % exchange_port
    print('run_broker_in_process', broker_name, broker_port, exchange_endpoint)
    broker = Broker(broker_name, broker_port, 0, exchange_endpoint=exchange_endpoint)
    broker.start()
    print('Broker module started.')
    try:
        while True:
            time.sleep(9999)
    except KeyboardInterrupt:
        broker.stop()


main()
