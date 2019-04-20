"""Common utilities or code snippets."""

import threading
from collections import deque


class Incrementer:
    """A simple thread-/process-safe counter."""

    def __init__(self, init_value=0, lock=threading.Lock()):
        self._value = init_value
        self._lock = lock

    @property
    def value(self):
        """Current value of the counter."""
        return self._value

    def next(self):
        """Increments the current value by 1 and returns the updated value."""
        with self._lock:
            self._value += 1
            return self._value


class BatchMessenger:
    """A message queue that allows pushed messages to be popped in batches
    with an incrementing batch ID in a thread-safe way.
    """

    def __init__(self, maxlen=None):
        self._deque = deque(maxlen=maxlen)
        self._batch_id = 0
        self._lock = threading.RLock()

    def start_batch(self):
        """Requires to pop a batch of messages from this queue.

        Tries to acquire a lock to ensure only the caller thread can pop
        messages after this function returns. Will block if another thread
        is in a batch.

        Returns the batch ID.
        """
        self._lock.acquire()
        return self._batch_id

    def end_batch(self):
        """Notifies the end of the current batch.

        Releases the internal lock so that other threads can pop a new
        batch of messages.
        """
        self._batch_id += 1
        self._lock.release()

    def push(self, message):
        """Pushes a new message to the queue."""
        self._deque.append(message)

    def pop(self):
        """Pops a message from the queue.

        Raises IndexError if the queue is empty.
        """
        with self._lock:
            return self._deque.popleft()

    @property
    def is_empty(self):
        """Whether the message queue is empty."""
        return not self._deque


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
