#!/bin/bash

cd ..

for (( i = 1; i <= 10; i++ )); do
    /opt/anaconda3/bin/python3 -m peacock.test.trader_kun_multi_trader $i $i $i &
done
