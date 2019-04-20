import sys
import grpc
from .._pyprotos import broker_pb2 as pb2
from .._pyprotos import common_pb2
import time
from random import randint
import random
from .._pyprotos.broker_pb2_grpc import BrokerStub
from .._pyprotos.market_data_pb2_grpc import MarketDataStub
from .._pyprotos.common_pb2 import (
    OK, SERVICE_UNAVAILABLE, REGISTER_DISABLED, ACCOUNT_DISABLED,
    UNAUTHORIZED, TOO_MANY_REQUESTS, TOO_MANY_ORDERS, INVALID_TRADER_NAME, INVALID_TRADER_ID,
    INVALID_PRICE, INVALID_SYMBOL, INVALID_SIDE, INVALID_POSITION,
    INVALID_VOLUME, INVALID_ORDER_ID, INVALID_REQUEST,
    INSUFFICIENT_ASSETS, ON_MARGIN_CALL
)

BROKER_ENDPOINT = 'localhost:52500'
MARKET_ENDPOINT = 'localhost:52600'


class ContestClient:
    def __init__(self, trader_id_, trader_pin_, broker_idx=0):
        self.ip = 'localhost'
        self.broker_port = 52500 + broker_idx
        self.broker_endpoint = '%s:%d' % (self.ip, self.broker_port)
        self.market_endpoint = '%s:52600' % self.ip
        self.trader_id = trader_id_
        self.trader_pin = trader_pin_

        self.market_channel = grpc.insecure_channel(self.market_endpoint)
        self.market_stub = MarketDataStub(self.market_channel)
        self.broker_channel = grpc.insecure_channel(self.broker_endpoint)
        self.broker_stub = BrokerStub(self.broker_channel)

        self.feed = self.market_stub.subscribe(common_pb2.Empty())
        print("client %d %s market:%s broker:%s" %
              (self.trader_id, self.trader_pin, self.market_endpoint, self.broker_endpoint))

    def next_market_data(self):
        snapshot = None
        while True:
            try:
                snapshot = next(self.feed)
                break
            except (grpc._channel._Rendezvous, KeyError) as err:
                print('meet market stream error, try reconnect', err)
                del self.feed
                del self.market_stub
                del self.market_channel
                self.market_channel = grpc.insecure_channel(self.market_endpoint)
                self.market_stub = MarketDataStub(self.market_channel)
                self.feed = self.market_stub.subscribe(common_pb2.Empty())
        return snapshot

    def req_new_order(self, request):
        try:
            t2 = time.time()
            response = self.broker_stub.new_order(request)
            elapsed2 = time.time() - t2
            print('new_order_latency {} {} buy'.format(elapsed2, self.trader_id), file=sys.stderr)
            return response
        except (grpc._channel._Rendezvous, KeyError) as err:
            return None

    def req_cacel_order(self, request):
        try:
            t2 = time.time()
            response = self.broker_stub.cancel_order(request)
            elapsed2 = time.time() - t2
            print('cancel_order_latency {} {} sell'.format(elapsed2, self.trader_id), file=sys.stderr)
            return response
        except (grpc._channel._Rendezvous, KeyError) as err:
            return None

    def next_market_data_error(self):
        for snapshot in self.feed:
            return snapshot

    def frequent_order_and_cancel(self):
        trader_request = pb2.TraderRequest(trader_id=self.trader_id, trader_pin=self.trader_pin,
                                           request_type=common_pb2.FULL_INFO)
        last_ts = 0
        count = 0
        while True:
            t1 = time.time()
            market_snapshot = self.next_market_data()
            elapsed1 = time.time() - t1
            if market_snapshot is None:
                continue
            # print(market_snapshot)
            print('market_latency {} {}'.format(elapsed1, self.trader_id), file=sys.stderr)

            t = time.time()
            if t - last_ts > 1:
                last_ts = t

                t0 = time.time()
                trader_info = self.broker_stub.get_trader(trader_request)
                elapsed0 = time.time() - t0
                print('traders_info_latency {} Error {}'.format(elapsed0, trader_info.result_code), file=sys.stderr)

            response = None
            for i in range(len(market_snapshot.instruments)):
                snapshot = market_snapshot.instruments[i]
                if snapshot.symbol == "A000.PSE" or snapshot.symbol == "B000.PSE":
                    continue
                bids = snapshot.bid_levels
                asks = snapshot.ask_levels
                bid_price1 = bids[0].price
                ask_price1 = asks[0].price
                mid_price = round((bid_price1 + ask_price1) / 2, 2)
                # count = randint(0, 4)
                dp = round(random.uniform(0.01, 1), 2)
                request = pb2.TraderRequest(trader_id=self.trader_id, trader_pin=self.trader_pin,
                                            request_type=common_pb2.NEW_ORDER, side=common_pb2.BID,
                                            symbol=snapshot.symbol, volume=11, price=(mid_price - 0.09),
                                            is_market=False, pos_type=common_pb2.LONG)
                # print(snapshot.symbol, "Buy", mid_price-0.09)
                response = self.req_new_order(request)

                if response and response.result_code == common_pb2.OK:
                    count += 1
                request = pb2.TraderRequest(
                    trader_id=trader_id, trader_pin=trader_pin, request_type=common_pb2.NEW_ORDER, side=common_pb2.ASK,
                    symbol=snapshot.symbol, volume=11, price=(mid_price + dp), is_market=False, pos_type=common_pb2.SHORT
                )

                # t3 = time.time()
                # response = self.broker_stub.new_order(request)
                # elapsed3 = time.time() - t3
                # print('new_order_latency {} {} sell'.format(elapsed3, self.trader_id), file=sys.stderr)
                response = self.req_new_order(request)
                if response and response.result_code == common_pb2.OK:
                    count += 1

            t0 = time.time()
            rsp = self.broker_stub.get_trader(pb2.TraderRequest(trader_id=trader_id, trader_pin=trader_pin,
                                                                request_type=common_pb2.FULL_INFO))
            elapsed0 = time.time() - t0
            print('traders_info_latency {} Error {}'.format(elapsed0, rsp.result_code), file=sys.stderr)

            if count > 100:
                count = 0
                for k, v in rsp.orders.orders.items():
                    request = pb2.TraderRequest(
                        trader_id=trader_id, trader_pin=trader_pin, request_type=common_pb2.CANCEL_ORDER,
                        order_id=v.order_id
                    )
                    response = self.req_cacel_order(request)
                    if response and response.result_code == common_pb2.OK:
                        print("Cancel {} successfully".format(v.order_id))
                    else:
                        print("Failed to cancel {}, error {}".format(v.order_id, response.result_code))

    def invalid_cancels(self):
        while True:
            request = pb2.TraderRequest(trader_id=self.trader_id, trader_pin=self.trader_pin,
                                        request_type=common_pb2.CANCEL_ORDER, order_id=5)
            response = self.broker_stub.cancel_order(request)
            if response.result_code == common_pb2.OK:
                print("Cancel {} successfully".format(5), file=sys.stderr)
            else:
                print("Failed to cancel {}".format(5), file=sys.stderr)


if __name__ == '__main__':
    # TRADER_ID is an integer, TRADER_PIN is a string
    trader_id = 1
    trader_pin = '1'
    broker_id = 0
    if len(sys.argv) < 4:
        pass
    else:
        trader_id = int(sys.argv[1])
        trader_pin = str(sys.argv[2])
        broker_id = int(sys.argv[3])

    client = ContestClient(trader_id, trader_pin, broker_id)
    client.frequent_order_and_cancel()
