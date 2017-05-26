#!/usr/bin/perl
use strict;
use warnings;

my @nums = ( 1 .. 10 );
my @squares = map { $_**2 } @nums;
print "@squares\n";
