#!/bin/bash

perl -c                     # check but donot execute
perl -d                     # run under debugger control
perl -MO=Lint a.pl          # syntax check

sudo apt install libdevel-dprof-perl
# profiling
perl -d:DProf slow.pl
dprofpp

# code coverage
perl -d:Coverage covered.pl < input1
perl -d:Coverage covered.pl < input2
coverperl covered.pl.cvp
