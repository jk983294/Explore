#!/usr/bin/perl
use strict;
use warnings;

my $a = "abc";
my $b = "def";
my $d = 10;

my $c = $a . $b;    # abcdef
$c = "-" x 3;       # ---
my @c = ( 2 .. 5 ); # [2 3 4 5]
$d++;               # 11
$d--;               # 10
