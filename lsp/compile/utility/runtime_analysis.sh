#!/bin/bash

# addr2line analysis core-dump
# get crash pc
addr2line -C -f -e main_dynamic 0x400730

# find entry point of dynamic lib when running
LD_DEBUG=files gdb -q ./main_dynamic
b main
r
set disassembly-flavor intel
disassemble 0x00007ffff6f6ca70

# find dynamic libs
ps -ef | grep bash  # find pid
cat /proc/1896/maps
