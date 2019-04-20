"""Simple Clock class for Peacock's virtual timeline."""

from datetime import datetime
import threading


class Clock:
    """A clock that keeps its own timeline."""

    def __init__(self, time_speedup=1.0):
        self._speedup = time_speedup
        self._start_utc = datetime.now().timestamp()
        self._epoch_utc = datetime(2018, 1, 1).timestamp()

    @property
    def timestamp(self):
        """The current timestamp."""
        real_elapsed = datetime.now().timestamp() - self._start_utc
        return real_elapsed * self._speedup

    def __str__(self):
        dt = datetime.fromtimestamp(self._epoch_utc + self.timestamp)
        return dt.strftime('Day %d %H:%M:%S')


class PausableClock(object):
    """Measures the flow of time in a virtual timeline."""

    def __init__(self):
        self._last_ts = 0.0
        self._last_real_ts = datetime.utcnow().timestamp()
        self._is_paused = False
        self._lock = threading.Lock()

    def timestamp_now(self):
        """Returns elapsed seconds (as float) in this clock."""
        self._lock.acquire()
        ts_now = self._last_ts
        if not self._is_paused:
            ts_now = self._last_ts + datetime.utcnow().timestamp() - self._last_real_ts
        self._lock.release()
        return ts_now

    def is_paused(self):
        """Returns whether the clock is paused now."""
        return self._is_paused

    def pause(self):
        """Pauses the time flow in this clock."""
        self._lock.acquire()
        if not self._is_paused:
            self._is_paused = True
            real_ts = datetime.utcnow().timestamp()
            self._last_ts += real_ts - self._last_real_ts
            self._last_real_ts = real_ts
        self._lock.release()

    def resume(self):
        """Resumes the time flow in this clock."""
        self._lock.acquire()
        if self._is_paused:
            self._last_real_ts = datetime.utcnow().timestamp()
            self._is_paused = False
        self._lock.release()

    def reset(self):
        """Resets elapsed time in this clock to zero.

        Does not change pause state."""
        self._lock.acquire()
        self._last_ts = 0.0
        self._last_real_ts = datetime.utcnow().timestamp()
        self._lock.release()
