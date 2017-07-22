#!/bin/bash

# change DT_RPATH of elf file
chrpath

# change DT_RUNPATH for elf file
patchelf

# remove exported symbol
strip --strip-symbol _Z11print_firstv libdynamiclib.so
