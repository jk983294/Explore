#!/bin/bash

# list runtime dependency recurrisvly
# cannot find dlopen() loaded lib

ldd libdynamiclib.so                                # display all exported symbols in object files

# safe way to find dependency but not recurrisvly
objdump -p libdynamiclib.so | grep NEEDED
readelf -d libdynamiclib.so | grep NEEDED


ldconfig -p                                         # print all known libs, under /etc/ld.so.cache
ldconfig -p | grep boost                            # find given lib
ldconfig -p | grep boost | grep system

# find dlopen libs
lsof -p pid | grep "\.so"
