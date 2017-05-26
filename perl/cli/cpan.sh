#!/bin/bash

cpan -a                             # list all installed modules

cpan Moose                          # install Moose module
cpan Test::Class                    # install Test::Class

perl -MCPAN -e shell                # open cpan shell
> h                                 # help
> m                                 # list all modules
> d /bioperl/                       # list bioperl related modules
> install module_name               # install
> q                                 # quit
