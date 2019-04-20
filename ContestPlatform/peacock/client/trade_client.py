"""
A client class that performs trading operations by calling the Broker API.
"""

from collections import deque

import grpc

from .._pyprotos import common_pb2
from .._pyprotos import broker_pb2
from .._pyprotos import broker_pb2_grpc


class TradeClient:
    """
    A Simple trade client implementation.
    Encapsulates underlying gRPC calls for common trading operations.
    """

    def __init__(self, broker_endpoint=None, broker_stub=None):
        if broker_stub:
            # By providing Broker stubs as init args, multiple clients
            # can share the same stub.
            self._broker = broker_stub
            if broker_endpoint:
                print('[TraderClient] Ignoring endpoint when a stub is provided.')
        elif broker_endpoint:
            self._broker = broker_pb2_grpc.BrokerStub(grpc.insecure_channel(
                broker_endpoint
            ))

        self._trader_info = None    # broker_pb2.TraderInfo
        self._account = None        # broker_pb2.TraderAccount
        self._active_orders = {}    # order_id -> broker_pb2.OrderInfo
        self._long_positions = {}   # symbol -> broker_pb2.PositionInfo
        self._short_positions = {}  # symbol -> broker_pb2.PositionInfo

        self._last_timestamp = 0.0

    def register(self, name, pin=None, init_cash=0):
        """Registers a new trader account and, if successful, logs in.

        If the Broker does not allow custom initial cash, the param
        will be ignored.

        Returns whether the registration is successful.
        """
        request = broker_pb2.RegisterRequest(
            trader_name=name, trader_pin=pin or "", init_cash=init_cash
        )

        response = self._broker.register(request)

        self._logout()

        if response.result_code == common_pb2.OK:
            self._handle_response(response)
            return True
        else:
            print('Cannot register account (error: %d)' % response.result_code)
            return False

    def login(self, trader_id, pin):
        """Logs in an existing trader account.

        Returns whether the login is successful.
        """
        response = self._broker.get_trader(broker_pb2.TraderRequest(
            trader_id=trader_id, trader_pin=pin,
            request_type=common_pb2.FULL_INFO
        ))

        self._logout()

        if response.result_code == common_pb2.OK:
            self._handle_response(response)
            return True

        return False

    def _logout(self):
        self._trader_info = None
        self._account = None
        self._active_orders.clear()
        self._long_positions.clear()
        self._short_positions.clear()
        self._last_timestamp = 0.0

    @property
    def trader_id(self):
        """The Trader ID, or None if the client has not logged in."""
        return self._trader_info.trader_id if self._trader_info else None

    @property
    def trader_pin(self):
        """Passcode for authentication."""
        return self._trader_info.trader_pin if self._trader_info else None

    @property
    def trader_info(self):
        """Passcode for authentication."""
        return self._trader_info

    @property
    def account(self):
        return self._account

    @property
    def available_cash(self):
        return (self._account.total_cash + self._account.unrealized_pnl -
                self._account.locked_cash - self._account.occupied_cash)

    @property
    def total_value(self):
        return self._account.total_cash + self._account.unrealized_pnl

    @property
    def long_positions(self):
        return self._long_positions

    @property
    def short_positions(self):
        return self._short_positions

    @property
    def active_orders(self):
        return self._active_orders

    def order(self, side, symbol, volume, price=None, pos_type=common_pb2.LONG,
              orig_timestamp=None):
        """Places a new order. Returns a result code."""
        if self._trader_info is None:
            print('Please login first.')
            return

        response = self._broker.new_order(broker_pb2.TraderRequest(
            trader_id=self.trader_id, trader_pin=self.trader_pin,
            request_type=common_pb2.NEW_ORDER, side=side, symbol=symbol,
            volume=volume, price=price or 0, is_market=(price is None),
            pos_type=pos_type, orig_timestamp=orig_timestamp or 0
        ))

        self._handle_response(response)

        return response.result_code

    def cancel(self, order_id):
        """Cancels a previous order. Returns a ResultCode."""
        if self._trader_info is None:
            print('Please login first.')
            return

        response = self._broker.cancel_order(broker_pb2.TraderRequest(
            trader_id=self.trader_id, trader_pin=self.trader_pin,
            request_type=common_pb2.CANCEL_ORDER, order_id=order_id
        ))

        self._handle_response(response)

        return response.result_code

    def refresh(self):
        """Refresh account data explicitly."""
        if self._trader_info is None:
            print('Please login first.')
            return

        response = self._broker.get_trader(broker_pb2.TraderRequest(
            trader_id=self.trader_id, trader_pin=self.trader_pin,
            request_type=common_pb2.INCREMENTAL_INFO
        ))

        self._handle_response(response)

        return response.result_code

    def get_position(self, pos_type, symbol):
        if pos_type == common_pb2.LONG:
            return self._long_positions.get(symbol)
        else:
            return self._short_positions.get(symbol)

    def _handle_response(self, response: broker_pb2.TraderResponse):
        """Updates locally cached account and order info."""
        if response.timestamp < self._last_timestamp:
            return

        if response.HasField('info'):
            self._trader_info = response.info

        if response.HasField('account'):  # broker_pb2.TraderAccount
            new_account = response.account
            if self._account:
                self._account.total_cash = new_account.total_cash
                self._account.unrealized_pnl = new_account.unrealized_pnl
                self._account.locked_cash = new_account.locked_cash
                self._account.occupied_cash = new_account.occupied_cash
                self._account.realized_pnl = new_account.realized_pnl
                self._account.commission = new_account.commission
            else:
                self._account = new_account

        if response.HasField('positions'):
            self._long_positions.update(response.positions.long_positions)
            self._short_positions.update(response.positions.short_positions)

        for order_id, update in response.orders.orders.items():
            # Remove finished orders
            is_archived = update.state in (
                common_pb2.ORDER_CANCELLED, common_pb2.ORDER_FINISHED,
                common_pb2.ORDER_REJECTED
            )
            if order_id in self._active_orders and is_archived:
                del self._active_orders[order_id]
            elif not is_archived:
                self._active_orders[order_id] = update
