#!/usr/bin/perl
use strict;
use warnings;

# bitwise usually used for file ACL bit
my $a = 60;
my $b = 13;
my $c = $a & $b;    # 12
$c = $a | $b;       # 61
$c = $a ^ $b;       # 49
$c = ~$a;           # 18446744073709551555
$c = $a << 2;       # 240
$c = $a >> 2;       # 15
