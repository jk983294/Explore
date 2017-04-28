#!/usr/bin/perl
use strict;
use warnings;

# a {} represents any pair of delimiters you choose
# single quotes / double quotes / invert quotes; '' / "" / ``
my $a = 10;

my $b = q{a = $a};    # a = $a
$b = qq{a = $a};      # a = 10
my $t = qx{date};     # unix command execution, Thu Feb 14 08:13:17 MST 2013
