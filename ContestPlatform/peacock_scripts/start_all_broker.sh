#!/bin/bash

cd ..

for (( i = 1; i <= 10; i++ )); do
    /opt/anaconda3/bin/python3 -m peacock.broker 52500 $i 51701 &
done
