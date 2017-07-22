#!/bin/bash

# disassembly support two assembly format: (1) AT&T (2) Intel

objdump -D function.o
objdump -D -Mintel function.o          # disassembly object file
objdump -D -Mintel main                # disassembly binary execuable
objdump -d -Mintel libdynamiclib.so | grep -A 10 print_first    # disassembly and find print_first code
objdump -d -Mintel main_dynamic | grep -A 10 \<main\>           # disassembly and display main function
objdump -d -Mintel -j .plt main_dynamic                         # disassembly given section

objdump -f libdynamiclib.so             # dsiplay elf header info
objdump -t libdynamiclib.so             # display all symbols, the same with nm binary
objdump -T libdynamiclib.so             # display all exported symbols, the same with nm -D binary
objdump -h libdynamiclib.so             # display all sections
objdump -p libdynamiclib.so             # display dynamic sections and segment info
objdump -R libdynamiclib.so             # display dynamic relocation section
objdump -x -j .bss main                 # display bss section
