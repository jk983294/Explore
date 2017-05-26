#!/usr/bin/perl
use strict;
use warnings;
use Carp;

# warn user
carp "string trimmed to 80 chars";

# die of errors
croak "We're outta here!";

# die of errors with stack backtrace
confess "not implemented";
