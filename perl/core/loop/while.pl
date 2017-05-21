#!/usr/bin/perl
use strict;
use warnings;

my $a = 10;
while ( $a < 13 ) {
    printf "Value of a: $a\n";
    $a = $a + 1;
}

print " ", ( $a += 2 ) while $a < 16;
