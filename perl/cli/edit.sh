#!/bin/bash

# -p        means print  while(<>){ print; }
# -i        $^I='.bak'
# -w        warning
# -e        executable code, it will insert before print statement
perl -p -i.bak -w -e 's/kun/jk/gi' ~/log
