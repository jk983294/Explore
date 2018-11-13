#!/bin/bash

for (( i = 0; i < 25; i++ )); do
    ../contest/cpp_client/install/client_main $i 123456 &
done
