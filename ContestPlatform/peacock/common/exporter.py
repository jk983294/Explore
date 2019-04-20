"""
Export various data to file.
"""

import datetime

# Maps symbol to tick data list.
_TICK_DATA = {}

_ACCOUNT_DATA = {}

_BUFFER_SIZE = 100


class _TickData(object):
    def __init__(self, timestamp, price, volume):
        self.time = datetime.datetime.fromtimestamp(timestamp)
        self.price = price
        self.volume = volume

    def __str__(self):
        return '%s, %.2f, %d' % (
            self.time.strftime('%Y%m%d %H:%M:%S.%f'[:-3]),
            self.price, self.volume)


def write_tick(timestamp, symbol, price, volume):
    """Write a tick data for an instrument."""
    filename = '%s.log' % (symbol)

    if symbol not in _TICK_DATA:
        _TICK_DATA[symbol] = []
        with open(filename, 'w') as _:
            pass
    data_list = _TICK_DATA[symbol]

    data_list.append(_TickData(timestamp, price, volume))

    if len(data_list) >= _BUFFER_SIZE:
        # Write buffered data to file.
        with open(filename, 'a') as file:
            for item in data_list:
                file.write(item.__str__())
                file.write('\n')
        del data_list[:]  # remove all


class _AccountData(object):
    def __init__(self, timestamp, cash, total_value):
        self.time = datetime.datetime.fromtimestamp(timestamp)
        self.cash = cash
        self.total_value = total_value

    def __str__(self):
        return '%s, %.2f, %.2f' % (
            self.time.strftime('%Y%m%d %H:%M:%S.%f'[:-3]),
            self.cash, self.total_value)


def write_pnl(timestamp, trader_id, cash, total_value):
    """Write a tick data for an instrument."""
    filename = 'PNL_%d.log' % (trader_id)

    if trader_id not in _ACCOUNT_DATA:
        _ACCOUNT_DATA[trader_id] = []
        with open(filename, 'w') as _:
            pass
    data_list = _ACCOUNT_DATA[trader_id]

    data_list.append(_AccountData(timestamp, cash, total_value))

    if len(data_list) >= _BUFFER_SIZE:
        # Write buffered data to file.
        with open(filename, 'a') as file:
            for item in data_list:
                file.write(item.__str__())
                file.write('\n')
        del data_list[:]  # remove all


def _flush():
    for symbol, data_list in _TICK_DATA.items():
        filename = '%s.log' % (symbol)
        with open(filename, 'a') as file:
            for item in data_list:
                file.write(item.__str__())
                file.write('\n')

    for trader_id, data_list in _ACCOUNT_DATA.items():
        filename = 'PNL_%d.log' % (trader_id)
        with open(filename, 'a') as file:
            for item in data_list:
                file.write(item.__str__())
                file.write('\n')
