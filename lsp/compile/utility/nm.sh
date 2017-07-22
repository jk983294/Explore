#!/bin/bash

# list symbols from object files
# A     Global absolute symbol
# a     Local absolute symbol
# B     Global bss symbol
# b     Local bss symbol
# D     Global data symbol
# d     Local data symbol
# f     Source file name symbol
# L     Global thread-local symbol (TLS)
# l     Static thread-local symbol (TLS)
# T     Global text symbol
# t     Local text symbol
# U     Undefined symbol

nm libdynamiclib.so                         # display all symbols
nm -n libdynamiclib.so                      # list all the symbols in sorted with the undefined symbols first and then according to the addresses
nm --size-sort libdynamiclib.so             # sort by size
nm -D libdynamiclib.so                      # display all exported symbols in object files
nm -C libdynamiclib.so                      # list unchanged symbol name, usually more straight forward
nm -D --no-demangle libdynamiclib.so        # print mangled symbols, useful to check extern C identifier
nm -DA * | grep print_first                 # display object files that refer to a symbol
nm -u libdynamiclib.so                      # list all un-resolved and week symbol
nm -S libdynamiclib.so | grep print_first   # display size of a given symbol
nm -u -f posix libdynamiclib.so             # display the output of nm command in posix style
nm -g libdynamiclib.so                      # lists only the external symbols
