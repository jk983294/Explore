#!/usr/bin/perl
use strict;
use warnings;

my $a = 2;
my $b = 4;

my $c = $a + $b;
$c += $a;
$c -= $a;
$c *= $a;
$c /= $a;
$c %= $a;
$c**= $a;

my $str = "kun";
$str .= "\n";    # equals to $str = $str . "\n";
print $str
