#!/bin/bash

readelf --segments main                 # show segments of an elf
readelf -h main_dynamic                 # show elf header info
readelf -S main_dynamic                 # show sections
readelf --symbols main_dynamic          # display all symbols, the same with nm main_dynamic
readelf --dyn-syms libdynamiclib.so     # display all exported symbols in object files, the same with nm -D libdynamiclib.so
readelf -d main_dynamic                 # show dynamic section, like DT_RPATH DT_RUNPATH
readelf -r main_dynamic                 # show relocation section
readelf -x .got main_dynamic            # show hex dump of given section
readelf --segments main_dynamic         # show all segments
readelf --debug-dump=line main_dynamic | wc -l  # check binary built with debug option


readelf -h main_dynamic | grep Entry    # get entry point

# check if PIC or LTR, if compile with -fPIC, then no TEXTREL field
readelf -d libdynamiclib.so | grep TEXTREL
