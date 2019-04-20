#!/bin/bash

# generate grpc file
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/common.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/broker.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/broker_admin.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/exchange.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/market_data.proto
/opt/anaconda3/bin/python -m grpc_tools.protoc -I./peacock/protos --python_out=./peacock/_pyprotos --grpc_python_out=./peacock/_pyprotos ./peacock/protos/robot_pool.proto

# start server
p3 -m peacock peacock/etc/all_multi_brokers_template.xml
nohup /opt/anaconda3/bin/python3 -m peacock peacock/etc/all_multi_brokers_template.xml > /tmp/kun_peacock.log 2>&1  &
p3 -m peacock.broker
p3 -m peacock.broker 52500 31 51701
p3 PostClient.py localhost 52921 'results'

# start client
p3 -m peacock.test.trader_kun_multi_trader 6 6 6
p3 trader_kun_multi_trader.py 6 6 6 > player6.log 2>&1

# kill process
psg trader_kun | awk '{ print $2 }' | xargs kill
psg 'peacock.broker 52500' | awk '{ print $2 }' | xargs kill
psg python | grep defunct | awk '{ print $2 }' | xargs kill

# stats gathering
grep new_order_latency server.log | awk '{ if ($6 == 2){ print $0 } }' | less
grep market_latency player6.log | cut2 | stats
grep traders_info_latency player6.log | cut2 | stats
grep new_order_latency player6.log | cut2 | stats
grep cancel_order_latency player6.log | cut2 | stats
