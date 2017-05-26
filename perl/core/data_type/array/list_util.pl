#!/usr/bin/perl
use strict;
use warnings;
use List::Util qw(first sum max min shuffle);

# use grep to select elements
my @strs = qw( a b c d d e f a );
my $first_match = first {/d/} @strs;
print "$first_match\n";

my @nums      = ( 1 .. 10 );
my $total     = sum(@nums);
my $max_value = max(@nums);
my $min_value = min(@nums);
print "$total\n";
print "$max_value\n";
print "$min_value\n";
