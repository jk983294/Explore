"""A very simple logger."""

import threading


class Logger(object):
    """A very simple logger."""

    def __init__(self, filename, buffer_size=1000):
        self._buffer = []
        self._filename = filename
        self._buffer_size = buffer_size
        self._lock = threading.Lock()

    def __del__(self):
        print('[LOGGER] flushing before leaving.')
        self.flush()

    def append(self, log):
        """Add any item that implements __str__."""
        with self._lock:
            self._buffer.append(str(log))

        if len(self._buffer) >= self._buffer_size:
            self.flush()

    def flush(self):
        with self._lock:
            with open(self._filename, 'a') as file:
                for item in self._buffer:
                    file.write(item + '\n')
            del self._buffer[:]
