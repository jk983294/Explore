#!/usr/bin/perl
use strict;
use warnings;

my @nums = ( 1, 3, 9, 4, 7, 2 );

my @sorted = sort { $a <=> $b } @nums;
print "@sorted\n";    # 1 2 3 4 7 9

@sorted = sort { $b <=> $a } @nums;
print "@sorted\n";    # 9 7 4 3 2 1
