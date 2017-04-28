#!/usr/bin/perl
use strict;
use warnings;

my $a = 10;
LOOP1: do {
    if ( $a == 15 ) {    # skip the iteration.
        $a = $a + 1;
        goto LOOP1;      # use goto LABEL form
    }
    print "Value of a = $a\n";
    $a = $a + 1;
} while ( $a < 20 );

$a = 10;
my $str1 = "LO";
my $str2 = "OP";

LOOP: do {
    if ( $a == 15 ) {    # skip the iteration.
        $a = $a + 1;
        goto $str1 . $str2;    # use goto EXPR form
    }
    print "Value of a = $a\n";
    $a = $a + 1;
} while ( $a < 20 );
