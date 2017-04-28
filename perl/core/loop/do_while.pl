#!/usr/bin/perl
use strict;
use warnings;

$a = 10;
do {
    printf "Value of a: $a\n";
    $a = $a + 1;
} while ( $a < 13 );
