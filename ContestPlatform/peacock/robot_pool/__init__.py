"""
Peacock Robot Pool Module
"""

import threading
import datetime
import importlib
import pprint
from concurrent import futures
from xml.etree import ElementTree
from os import path

import grpc

from .._pyprotos import (
    common_pb2, robot_pool_pb2 as pb2, robot_pool_pb2_grpc as pb2_grpc
)
from .._pyprotos.broker_pb2_grpc import BrokerStub
from .._pyprotos.market_data_pb2_grpc import MarketDataStub
from ..client import MarketClient
from .robot import Robot, SharedInfoKey as SIKey


def _step_robot(robot: Robot):
    robot.on_step()


class _RobotRunner(threading.Thread):
    """Keeps the Robots running unless the user stops it.

    Attributes:
        cancelled: False by default. Can be set to True to stop the running
            loop.
        robots (list): List of Robot instances.
        total_steps: Total number of steps executed in this run.
    """

    def __init__(self, robots, shared_info, max_worker_threads=None):
        super(_RobotRunner, self).__init__()
        self._cancelled = False
        self._robots = robots
        self._max_workers = max_worker_threads
        self._total_steps = 0
        self._total_reborns = 0
        self._shared_info = shared_info

    @property
    def total_steps(self):
        return self._total_steps

    @property
    def total_reborns(self):
        return self._total_reborns

    def start(self):
        self._total_steps = 0
        self._cancelled = False
        super(_RobotRunner, self).start()

    def stop(self):
        """Stops the robots from running."""
        print('Stopping robot runner...')
        self._cancelled = True

    def run(self):
        """Main running loop.

        Unless self.cancelled is set to True, the function calls each Robot's
        on_step() function repeatedly.
        """
        for robot in self._robots:
            robot.on_started()
        print('[ROBOT POOL] %d robots started (threads=%d).' %
              (len(self._robots), self._max_workers or 0))

        with futures.ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            while not self._cancelled:
                for _ in executor.map(_step_robot, self._robots):
                    pass  # Synchronize robots before next step
                self._total_steps += 1
                self._shared_info[SIKey.STEP_NUM] = self._total_steps

        for robot in self._robots:
            robot.on_stopped()
        print('[ROBOT POOL] %d robots stopped.' % len(self._robots))


class RobotPool(pb2_grpc.RobotPoolServicer):
    """Orchestrates a pool of trading robots.

    Robots in a pool share the same Broker/MarketData stubs.
    """

    def __init__(self, config_name, port=None,
                 broker_endpoint=None, broker_obj=None,
                 market_data_endpoint=None, market_data_obj=None):

        if broker_obj:
            # Access Broker object in local memory
            self._broker = broker_obj
        elif broker_endpoint:
            # Access remote Broker through gRPC stub
            self._broker = BrokerStub(
                grpc.insecure_channel(broker_endpoint)
            )
        else:
            raise ValueError("Broker not specified when init RobotPool.")

        if market_data_obj:
            # Access MarketData object in local memory
            self._market_data = market_data_obj
        elif market_data_endpoint:
            # Access remote MarketData through gRPC stub
            self._market_data = MarketDataStub(
                grpc.insecure_channel(market_data_endpoint)
            )
        else:
            raise ValueError("MarketData not specified when init RobotPool.")

        self._server = None
        self._port = port

        self._config_name = config_name

        self._runner = None

        self._shared_info = {
            SIKey.STEP_NUM: 0
        }   # Custom data shared by all bots in this pool.
        self._market_client = MarketClient(market_data_stub=self._market_data)

        self._robots = []
        self._max_worker_threads = 1  # TODO: read from XML

        self._load_config()

        self._error_message = ""

        self._last_step_count = 0
        self._last_update_time = 0
        self._last_frequency = 0

    # RobotPoolServicer

    def status(self, request=common_pb2.Empty(), _=None):
        now = datetime.datetime.now().timestamp()
        if now - self._last_update_time > 1:
            delta = self._runner.total_steps - self._last_step_count
            self._last_frequency = delta / (now - self._last_update_time)
            self._last_update_time = now
            self._last_step_count = self._runner.total_steps

        return pb2.PoolStatusResponse(
            is_running=self._runner and self._runner.is_alive(),
            error_message=self._error_message,
            total_robots=len(self._robots),
            frequency=self._last_frequency,
            total_reborns=self._runner.total_reborns
        )

    def reload(self, request=common_pb2.Empty(), _=None):
        """Reloads Robots from the config file.

        All currently running Robots will be stopped.
        """
        self.stop()

        print('Reloading "%s"' % self._config_name)
        return pb2.PoolStatusResponse()

    def start(self, request=common_pb2.Empty(), _=None):
        if self._runner and self._runner.is_alive():
            raise NotImplementedError

        self._runner = _RobotRunner(
            self._robots, self._shared_info, self._max_worker_threads
        )
        self._runner.start()
        return pb2.PoolStatusResponse()

    def stop(self, request=common_pb2.Empty(), _=None):
        if self._runner and self._runner.is_alive():
            self._runner.stop()
            self._runner.join()  # Wait until fullly stopped.

            self._market_client.disconnect()
        return pb2.PoolStatusResponse()

    def start_server(self):
        """Creates and starts a server that hosts the gRPC servicer."""
        if not self._port:
            print('Server port not specified.')
            return

        if self._server:
            raise NotImplementedError
        self._server = grpc.server(futures.ThreadPoolExecutor())
        pb2_grpc.add_RobotPoolServicer_to_server(self, self._server)

        self._server.add_insecure_port('[::]:%d' % self._port)
        self._server.start()

        print('[POOL %s] started service on port %d.' % (
            self._config_name, self._port))

    def stop_server(self):
        """Stops the server that hosts the gRPC servicer."""
        if self._server:
            self._server.stop(0)

        print('[POOL %s] stopped service.' % self._config_name)

    def print_shared_info(self):
        """Outputs shared info dict for debugging."""
        if self._shared_info:
            print('[POOL %s] shared info:' % self._config_name)
            pprint.pprint(self._shared_info)

    # Helper functions

    def _load_config(self):
        """Loads the config XML and initializes robots."""
        assert not self._runner or not self._runner.is_alive()
        assert not self._robots

        xml_filename = path.join(path.dirname(__file__),
                                 self._config_name + '.xml')

        xml_root = ElementTree.parse(xml_filename).getroot()

        # Load common parameters
        trader_pin = xml_root.find('trader_pin').text

        node = xml_root.find('max_worker_threads')
        if node is not None:
            self._max_worker_threads = int(node.text)

        for xml_node in xml_root.find('robots').findall('robot'):
            module_name = xml_node.get('module')
            module = importlib.import_module('.robots.%s' % module_name,
                                             'peacock.robot_pool')
            class_name = self._get_class_name(module_name)
            robot_class = getattr(module, class_name)

            count = int(xml_node.get('num', 1))

            for i in range(count):
                # The Robots share access to Broker and MarketData stubs.
                self._robots.append(
                    robot_class(
                        shared_info=self._shared_info,
                        broker_stub=self._broker,
                        market_client=self._market_client,  # sharing market client
                        name='%s-%d' % (class_name, i), pin=trader_pin,
                        xml_node=xml_node
                    )
                )
                # TODO: check whether account registration is successful

    def _get_class_name(self, module_name):
        """Converts a module name like_this to a class name LikeThis."""
        return ''.join([word.capitalize() for word in module_name.split('_')])
