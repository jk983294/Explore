#!/bin/bash

ar -rcs libstaticlib.a first.o second.o     # create static lib
ar -t libstaticlib.a                        # display object files contained
ar -x libstaticlib.a                        # extract object files contained
ar -d libstaticlib.a first.o                # remove first.o
ar -r libstaticlib.a first.o                # add first.o
