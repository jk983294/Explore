"""Helper classes for multi-processing."""

import multiprocessing as mp


def close_conn(conn: mp.connection.Connection):
    """Close a connection of a pipe."""
    try:
        conn.send(None)
        conn.close()
    except (KeyboardInterrupt, BrokenPipeError, OSError):
        # The other end may have already closed
        pass


def send_to(conn: mp.connection.Connection, message):
    """Try to send data through a connection, ignoring any exception."""
    if conn:
        try:
            conn.send(message)
        except (KeyboardInterrupt, BrokenPipeError, OSError):
            pass


class UnhandledTaskError(mp.ProcessError):
    """The TaskRunner receives a task that it cannot handle."""
    pass


class TaskRunner(mp.Process):
    """Abstract worker running in a sub process.

    The TaskRunner communicates with other processes through Pipes.

    When started, the TaskProcessor keeps getting tasks from the receiver ends
    of the input pipes, then call the process_task() method (to be overridden
    in subclasses).

    The class also provides some functions that are meant to be called by the
    parent process to manipulate this runner.

    A None object being sent through the pipe acts as an EOF signal.
    """

    def __init__(self, aux_conns=None, name=None):
        super().__init__(name=name)
        # Create a default pipe for other processes to communicate with this.
        self._outer_conn, self._inner_conn = mp.Pipe(duplex=True)
        self._listen_conns = [self._inner_conn]

        # There can be more than one task sources.
        if aux_conns:
            self._listen_conns += aux_conns

        self._add_task_lock = mp.Lock()
        self._get_result_lock = mp.Lock()

    @property
    def connection(self):
        """The default connection that other processes can use to communicate
        with this sub process.

        Note: if more than one processes will send data via this connection
        simultaneously, the data may be corrupted. Use add_task() function
        which is process-safe.
        Similarly, reading data from this connection is not process-safe. Use
        get_task() for a process-safe version.
        """
        return self._outer_conn

    def add_task(self, task):
        """Called by other processes to add a new task to be processed.

        The task can be any picklable object. It will be send through the
        outer end of the default pipe.
        """
        with self._add_task_lock:
            self._outer_conn.send(task)

    def get_result(self):
        """Called by other processes to get a processing result (if any).

        TODO: implement timeout
        """
        with self._get_result_lock:
            return self._outer_conn.recv()

    def stop(self):
        """Called by other processes to stop this runner by closing the
        default pipe.

        If there are other task pipes, the runner may not exit until all
        these pipes are closed.
        """
        with self._add_task_lock:
            self._outer_conn.send(None)
            self._outer_conn.close()

    def run(self):
        """Sub-process logic."""
        # Close the sender end this process inherited from its parent because
        # it is reserved for other processes to use.
        self._outer_conn.close()

        # Keeps polling tasks from receivers until all connections are closed.
        # Closed connections are removed from self._recv_conns.
        timeout = None
        while self._listen_conns:
            try:
                ready_conns = mp.connection.wait(self._listen_conns, timeout)
            except KeyboardInterrupt:
                # Ignore the interrupt, let parent process handle it.
                continue

            if not ready_conns:
                break

            for conn in ready_conns:
                try:
                    task = conn.recv()
                    if task is None:
                        # None is considered EOF because closing the pipe from
                        # the other end may not be sufficient due to the file
                        # descriptor inheritance issue.
                        raise EOFError
                except EOFError:
                    # A connection is closed. If it's an auxiliary connection,
                    # remove it from the connection list. If it is the default
                    # connection, set the wait timeout to 0 to process the
                    # remaining tasks in the auxiliary connections in a non-
                    # blocking way.
                    if conn is self._inner_conn:
                        timeout = 0
                    self._listen_conns.remove(conn)
                else:
                    # Handle task
                    self._process_task(task)

        # Notify the actual task handler that there is no more task so that it
        # can do necessary clean-ups, like notifying down-stream runners.
        self._on_stop()

    def _process_task(self, task):
        """Called by the runner subprocess to handle an incoming task.

        To be overridden by subclasses.
        """
        raise NotImplementedError('Subclass must override process_task(task)')

    def _on_stop(self):
        """Called by the runner subprocess before it stops.

        To be overridden by subclasses."""
        pass
