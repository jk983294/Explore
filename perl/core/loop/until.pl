#!/usr/bin/perl
use strict;
use warnings;

$a = 5;
until ( $a > 10 ) {
    printf "Value of a: $a\n";
    $a = $a + 1;
}
