"""Peacock Market Simulation Framework"""

import enum
import sys
import time
import os.path as path
from xml.etree import ElementTree
from multiprocessing import Pool
from .common.PostClient import PostClient
import json
from threading import Thread
import requests

import multiprocessing
import subprocess

import netifaces as ni

from .exchange import Exchange
from .broker import Broker
from .market_data import MarketData
from .robot_pool import RobotPool
from .post_server import PostServer


def get_local_ip():
    """Returns the IP of the local host as seen by a remote host."""
    for name in ni.interfaces():
        # Find the first non-loop-back IPv4 address
        addresses = ni.ifaddresses(name)
        if ni.AF_INET in addresses:
            address = addresses[ni.AF_INET][0]
            if 'broadcast' in address:
                return address['addr']
    return 'localhost'  # Cannot get local IP.


class ServerInfo(object):
    def __init__(self, is_remote, address, port):
        self.is_remote = is_remote
        self.address = address
        self.port = port

    @property
    def endpoint(self):
        return self.address + ':' + str(self.port)

    @classmethod
    def local(cls, port):
        return ServerInfo(False, get_local_ip(), port)

    @classmethod
    def remote(cls, endpoint):
        """Returns a remote module info with endpoint like '10.18.0.123:56789'."""
        try:
            parts = endpoint.split(':')
            assert len(parts) is 2
            address = parts[0]
            port = int(parts[1])

            return ServerInfo(True, address, port)
        except (AttributeError, ValueError, AssertionError):
            raise ValueError('Invalid endpoint format.')


def generate_broker_config(broker_index, broker_name, account_name, account_pin):
    with open("./peacock/broker/%s.xml" % broker_name, "wt") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<peacock>\n')
        f.write('   <broker id="%d" name="%s" allows_register="true" pin_length="6" thread_count="1" margin_rate="0.2">\n' % (
            broker_index, broker_name))
        f.write('   <default_account cash="1000000" />\n')
        f.write('   <commission rate="0.0001" />\n')
        f.write('   <accounts><account name="%s" pin="%s"/></accounts>\n' % (account_name, account_pin))
        f.write('   </broker>\n')
        f.write('</peacock>\n')


class TraderData(Thread):
    def __init__(self):
        super().__init__()
        self.traders = {}
        self.clients = []
        for i in range(34):
            broker_post_port = 51100 + i + 1
            self.clients.append(PostClient('localhost', broker_post_port))

    def run(self):
        while True:
            try:
                time.sleep(1)
                self.poll_broker()
            except KeyboardInterrupt:
                break
        print('stopping poll data from broker...')

    def poll_broker(self):
        for client in self.clients:
            time.sleep(0.1)
            try:
                result = client.post('results', {'type': 'query'}, json.loads('{}'))
                if result['status']:
                    for entry in result['result']:
                        self.traders[entry['trader_id']] = entry
            except:
                pass


def run_modules(config_filename):
    """Run modules as configured in the given XML file."""
    if not path.exists(config_filename):
        print('ERROR: Config file does not exist.')
        return

    try:
        tree = ElementTree.parse(config_filename).getroot().find('modules')
        assert tree, 'Node "modules" does not exist.'
    except (ElementTree.ParseError, AssertionError):
        print('ERROR: Invalid config file.')
        return

    print('Starting modules...')

    # Server endpoints of known modules, indexed by module name.
    server_info = {}

    # Exchange module does not depend on other modules.
    # It only needs a service port to be specified.

    exchange = None
    for node in tree.findall('exchange'):
        if exchange:
            print('WARNING: Only one Exchange per host allowed.')
            break
        try:
            port = int(node.find('port').text)
        except (AttributeError, ValueError):
            print('ERROR: Exchange must specify a port.')
            return

        try:
            exchange = Exchange(port)
            exchange.start()
        except:
            print('ERROR: Failed to start Exchange.')
            if exchange:
                exchange.stop()
                del exchange
            return

        server_info['exchange'] = ServerInfo.local(port)

    # Broker modules depend on Exchange module.
    # If a local Exchange object does not exist, the endpoint of a
    # remote Exchange service must be specified.
    # There can be more than one Brokers, provided they each have
    # a unique name and service ports.

    brokers = {}
    for node in tree.findall('broker'):
        try:
            name = node.find('name').text
            assert name, "Broker must have a name."
            assert name not in brokers, "Duplicated Broker name."

            port = int(node.find('port').text)
            # admin_port = int(node.find('admin_port').text)

            brokers[name] = Broker(name, port, 0, exchange_obj=exchange)
        except (AssertionError, AttributeError, ValueError) as err:
            print('ERROR: Cannot initialize Broker. (%s)' % str(err))
            break

        server_info['broker(%s)' % name] = ServerInfo.local(port)

    for node in tree.findall('broker_template'):
        name_prefix = node.find('name_prefix').text
        start_port = int(node.find('start_port').text)

        broker_index = 1
        accounts_node = node.find('accounts')
        if accounts_node:
            for account_node in accounts_node.findall('account'):
                account_name = account_node.get('name')
                account_pin = account_node.get('pin')

                broker_name = '%s%d' % (name_prefix, broker_index)
                broker_port = start_port + broker_index
                generate_broker_config(broker_index, broker_name, account_name, account_pin)
                server_info['broker(%s)' % broker_name] = ServerInfo.local(broker_port)
                broker_index += 1
        else:
            print('no accounts found')

    # MarketData module also depends on Exchange module.
    # Specify the Exchange endpoint if no local object exists.
    # There should be only one MarketData instance.

    market_data = None
    for node in tree.findall('market_data'):
        if market_data:
            print('WARNING: Only one MarketData per host allowed.')
            break
        try:
            port = int(node.find('port').text)

            if not exchange:
                endpoint = None
                # Exchange is remote, Endpoint is required.
                if node.find('remote_exchange') is not None:
                    endpoint = node.find('remote_exchange').text
                    if 'exchange' in server_info:
                        print('WARNING: Overwriting Exchange server info.')
                    server_info['exchange'] = ServerInfo.remote(endpoint)
                elif 'exchange' in server_info:
                    # If a previous Broker has already specified the remote
                    # Exchange endpoint, it can be used here.
                    endpoint = server_info['exchange'].endpoint

                market_data = MarketData(port, exchange_endpoint=endpoint)
            else:
                # Exchange is local. Endpoint is ignored.
                if node.find('remote_exchange') is not None:
                    print('WARNING: Preferring local Exchange over remote.')
                market_data = MarketData(port, exchange_obj=exchange)
        except (AssertionError, AttributeError, ValueError) as err:
            print('ERROR: Cannot initialize MarketData. (%s)' % str(err))
            break

        server_info['market_data'] = ServerInfo.local(port)

    # Before parsing RobotPools, now we have to start the services of
    # local Brokers and MarketData (if any).

    try:
        for broker_ in brokers.values():
            broker_.start()

        if market_data:
            market_data.start()
    except:
        print('ERROR: Failed to start Broker/MarketData service.')
        for broker_ in brokers.values():
            broker_.stop()
        brokers.clear()

        if market_data:
            market_data.stop()
            del market_data

        if exchange:
            exchange.stop()
            del exchange

    # RobotPools depend on both Broker and MarketData modules.
    # For each dependency, either a local object or a remote endpoint
    # must be provided to initialize a robot pool.
    # There can be more than one RobotPools running simultaneously, but
    # they must have distinct ports.

    robot_pools = {}
    for node in tree.findall('robot_pool'):
        try:
            name = node.find('name').text
            assert name, "RobotPool must have a name."
            assert name not in robot_pools, "Duplicated RobotPool name."

            port = int(node.find('port').text)

            broker_ = None
            broker_endpoint = None

            if node.find('broker_name') is not None:
                # Use the named local Broker
                broker_name = node.find('broker_name').text
                assert broker_name in brokers, "Broker name does not exist locally."
                broker_ = brokers[broker_name]
            elif node.find('remote_broker') is not None:
                # Use the specified remote Broker
                broker_endpoint = node.find('remote_broker').text
                server_info['broker(%s)' % broker_endpoint] = ServerInfo.remote(broker_endpoint)
            elif len(brokers) == 1:
                # Use the only local Broker
                broker_ = next(iter(brokers.values()))
            else:
                raise AttributeError('Broker not specified for RobotPool.')

            if not market_data:
                # MarketData is remote. Endpoint is required.
                md_endpoint = node.find('remote_market_data').text
                server_info['market_data'] = ServerInfo.remote(md_endpoint)

                robot_pools[name] = RobotPool(name, port, broker_endpoint, broker_, market_data_endpoint=md_endpoint)
            else:
                # MarketData is local. Endpoint is ignored.
                if node.find('remote_market_data'):
                    print('WARNING: Preferring local MarketData over remote.')
                robot_pools[name] = RobotPool(name, port, broker_endpoint, broker_, market_data_obj=market_data)
        except (AssertionError, AttributeError, ValueError) as err:
            print('ERROR: Cannot initialize RobotPool. (%s)' % str(err))
            break

        server_info['robot_pool(%s)' % name] = ServerInfo.local(port)

    try:
        for pool in robot_pools.values():
            pool.start_server()
            pool.start()
    except:
        print('ERROR: Failed to start RobotPool.')
        for pool in robot_pools.values():
            pool.stop_server()
        robot_pools.clear()

        for broker_ in brokers.values():
            broker_.stop()
        brokers.clear()

        if market_data:
            market_data.stop()
            del market_data

        if exchange:
            exchange.stop()
            del exchange

    trader_data = TraderData()
    global_info = {
        'brokers': brokers,
        'exchange': exchange,
        'trader_data': trader_data
    }
    post_server_ = PostServer('0.0.0.0', 52922, global_info)
    post_server_.start()
    trader_data.start()

    # Print server endpoints...
    print('┌────────────────────────────────────────────────────────┐')
    print('│                                                        │')
    print('│  Endpoints:                                            │')
    print('│                                                        │')
    for name in sorted(server_info.keys()):
        print('│  %30s: %-22s│' % (name, server_info[name].endpoint))
    print('│                                                        │')
    print('└────────────────────────────────────────────────────────┘')

    # Now wait until someone interrupted.
    try:
        while True:
            if exchange:
                exchange.print_status()

            time.sleep(3)
    except KeyboardInterrupt:
        print('\nUser interrupted.')
    finally:
        print('Stopping everything...')

        # Stop the services in reverse order.

        for pool in robot_pools.values():
            pool.stop()
            pool.stop_server()
        robot_pools.clear()

        for broker_ in brokers.values():
            broker_.stop()
        brokers.clear()

        if market_data:
            market_data.stop()
            del market_data

        if exchange:
            exchange.stop()
            del exchange
