#!/usr/bin/perl
use strict;
use warnings;

use constant true  => 1;
use constant false => 0;

my $a = true;
my $b = false;
print '$a and $b is ' . ( $a and $b ) . "\n";    # 0
print '$a && $b is ' . ( $a && $b ) . "\n";      # 0
print '$a or $b is ' . ( $a or $b ) . "\n";      # 1
print '$a || $b is ' . ( $a || $b ) . "\n";      # 1
print 'not $b is ' . ( not($b) ) . "\n";         # 1
print '! $b is ' .   ( !($b) ) . "\n";           # 1
