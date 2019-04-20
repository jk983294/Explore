"""
A client class that accesses market data by calling the MarketData API.
"""

import threading

from collections import deque

import grpc

from .._pyprotos.market_data_pb2_grpc import MarketDataStub
from .._pyprotos.common_pb2 import (
    Empty, InstrumentInfo
)


class OHLCRecord:
    """Open, high, low, close prices and traded volume since a time."""

    def __init__(self, timestamp, price, curr_volume, prev_volume=None):
        self._timestamp = timestamp
        self._open = price
        self._close = price
        self._high = price
        self._low = price
        self._prev_volume = prev_volume or curr_volume
        self._curr_volume = curr_volume

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def open(self):
        return self._open

    @property
    def close(self):
        return self._close

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def volume(self):
        return self._curr_volume - self._prev_volume

    @property
    def total_volume(self):
        return self._curr_volume

    def to_tuple(self):
        return (
            self._timestamp, self._open, self._high, self._low,
            self._close, self.volume
        )

    def update(self, price, curr_volume):
        self._close = price
        if price < self._low:
            self._low = price
        elif price > self._high:
            self._high = price
        if curr_volume > self._curr_volume:
            self._curr_volume = curr_volume


class InstrumentData:
    """Everything about an instrument."""

    def __init__(self, info: InstrumentInfo):
        self.symbol = info.symbol
        self.name = info.name
        self.init_price = info.init_price
        self.tick = info.tick
        self._snapshots = deque(maxlen=2000)
        self._ohlc_history = deque(maxlen=10000)
        self._ohlc_lock = threading.Lock()
        self._ohlc_interval = 1.0  # second

        # Tracks latest prices for computing moving averages
        self._ma10 = MovingAverager(100)
        self._ma100 = MovingAverager(1000)
        self._ma1000 = MovingAverager(10000)

    @property
    def current(self):
        """Latest orderbook snapshot of this Instrument.

        The snapshot is of type market_data_pb2.OrderBookSnapshot
        """
        return self._snapshots[-1] if self._snapshots else None

    @property
    def ma10(self):
        """Moving average of the last 10 prices."""
        return self._ma10.value

    @property
    def ma100(self):
        """Moving average of the last 100 prices."""
        return self._ma100.value

    @property
    def ma1000(self):
        """Moving average of the last 1000 prices."""
        return self._ma1000.value

    def get_ohlc_history(self, max_count=1):
        """Returns last N OHLC records."""
        with self._ohlc_lock:
            # TODO: use more efficient iterator here
            count = min(max_count, len(self._ohlc_history) - 1)
            history = [
                rec.to_tuple()
                for i, rec in enumerate(reversed(self._ohlc_history))
                if i < count
            ]
            return reversed(history)

    def add_snapshot(self, snapshot):
        """Pushes a new snapshot."""
        self._snapshots.append(snapshot)
        self._ma10.append(snapshot.last_price)
        self._ma100.append(snapshot.last_price)
        self._ma1000.append(snapshot.last_price)

        with self._ohlc_lock:
            if not self._ohlc_history:
                # First record
                self._ohlc_history.append(OHLCRecord(
                    snapshot.timestamp, snapshot.last_price,
                    snapshot.traded_volume
                ))
            else:
                last = self._ohlc_history[-1]
                if snapshot.timestamp - last.timestamp > self._ohlc_interval:
                    # New record
                    self._ohlc_history.append(OHLCRecord(
                        snapshot.timestamp, snapshot.last_price,
                        snapshot.traded_volume, last.total_volume
                    ))
                else:
                    last.update(snapshot.last_price, snapshot.traded_volume)


class MarketClient:
    """A Simple market data client.

    To access the latest info of instrument 'A001.PSE', use:
        client.instruments['A001.PSE'].current

    """

    def __init__(self, market_data_endpoint=None, market_data_stub=None):
        self._channel = None
        if market_data_stub:
            self._market_data = market_data_stub
            if market_data_endpoint:
                print('[MarketClient] Ignoring endpoint when a stub is provided!')
        elif market_data_endpoint:
            self._channel = grpc.insecure_channel(market_data_endpoint)
            self._market_data = MarketDataStub(self._channel)
        else:
            raise ValueError('Endpoint and Stub cannot both be None.')

        self._symbols = []      # Sorted list of instrument symbols
        self._instruments = {}  # Symbol -> InstrumentData

        self._snapshot_feed = None
        self._updater = None
        self._update_count = 0  # Total number of updates received
        self._stopped = False
        try:
            self._instruments = {
                info.symbol: InstrumentData(info) for info in
                self._market_data.list_instruments(Empty()).instruments
            }
            self._symbols = sorted(list(self._instruments.keys()))

            self._updater = threading.Thread(target=self._update_snapshot)
            self._updater.start()
        except grpc.RpcError as error:
            print('RPC error:', str(error))
            print('Market data disconnected.')

    def __del__(self):
        self._stopped = True

    @property
    def is_connected(self):
        """True if the client is getting snapshots from the Market."""
        return self._updater and self._updater.is_alive()

    @property
    def symbols(self):
        """A sorted list of available instrument symbols."""
        return self._symbols

    @property
    def instruments(self):
        """A dict of InstrumentInfo indexed by symbol."""
        return self._instruments

    @property
    def update_count(self):
        """Total number of updates received from the Exchange."""
        return self._update_count

    def reconnect(self):
        if not self.is_connected:
            del self._snapshot_feed
            self._snapshot_feed = None
            self._updater = threading.Thread(target=self._update_snapshot)
            self._updater.start()

    def disconnect(self):
        """Forces the client to disconnect from the Market server."""
        if self._snapshot_feed:
            if hasattr(self._snapshot_feed, 'cancel'):
                # If MarketData is a memory object instead of a gRPC stub,
                # the feed is just a Python generator and does not have
                # a 'cancel' method.
                self._snapshot_feed.cancel()
            del self._snapshot_feed
            self._snapshot_feed = None
            if self._updater:
                self._updater.join()
        print('Market data disconnected.')

    # Internal helper functions.

    def _update_snapshot(self):
        try:
            if not self._symbols or not self._instruments:
                self._instruments = {
                    info.symbol: InstrumentData(info) for info in
                    self._market_data.list_instruments(Empty()).instruments
                }
                self._symbols = sorted(list(self._instruments.keys()))
            if not self._snapshot_feed:
                self._snapshot_feed = self._market_data.subscribe(Empty())

            for new_snapshot in self._snapshot_feed:
                for inst in new_snapshot.instruments:
                    self._instruments[inst.symbol].add_snapshot(inst)
                    #print("deliver {}".format(inst.deliver_price))

                self._update_count += 1

                if self._stopped or not self._snapshot_feed:
                    break

        except grpc.RpcError as error:
            pass  # print('Snapshot updater stopped. (%s)' % str(error))


class MovingAverager:
    """Calculates the moving average of a contantly updating series."""

    def __init__(self, n):
        self._queue = deque(maxlen=n)
        self._sum = 0.0
        self._average = None

    @property
    def value(self):
        """Moving average value."""
        return self._average

    def append(self, num):
        """Adds a new number and updates the moving average."""
        if len(self._queue) == self._queue.maxlen:
            # Queue full
            self._sum -= self._queue.popleft()

        self._sum += num
        self._queue.append(num)

        self._average = self._sum / len(self._queue)
