#!/bin/bash

cd ..

nohup /opt/anaconda3/bin/python3 -m peacock peacock/etc/all_multi_brokers_template.xml &

sleep 1

for (( i = 1; i <= 10; i++ )); do
    /opt/anaconda3/bin/python3 -m peacock.broker 52500 $i 51701 &
done

