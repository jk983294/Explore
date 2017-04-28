#!/usr/bin/perl
use strict;
use warnings;

my $a = 21;
my $b = 10;
print '$a == $b is ' .  ( $a == $b ) . "\n";
print '$a != $b is ' .  ( $a != $b ) . "\n";
print '$a <=> $b is ' . ( $a <=> $b ) . "\n";
print '$a > $b is ' .   ( $a > $b ) . "\n";
print '$a >= $b is ' .  ( $a >= $b ) . "\n";
print '$a < $b is ' .   ( $a < $b ) . "\n";
print '$a <= $b is ' .  ( $a <= $b ) . "\n";

# String Equality Operators
$a = "abc";
$b = "xyz";
print '$a lt $b is ' .  ( $a lt $b ) . "\n";    # <
print '$a gt $b is ' .  ( $a gt $b ) . "\n";    # >
print '$a le $b is ' .  ( $a le $b ) . "\n";    # <=
print '$a ge $b is ' .  ( $a ge $b ) . "\n";    # >=
print '$a eq $b is ' .  ( $a eq $b ) . "\n";    # ==
print '$a ne $b is ' .  ( $a ne $b ) . "\n";    # !=
print '$a cmp $b is ' . ( $a cmp $b ) . "\n";
