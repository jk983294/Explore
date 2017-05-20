#!/usr/bin/perl
use strict;
use warnings;

# A continue BLOCK is always executed just before the conditional is about to be evaluated again
my $a = 0;
while ( $a < 3 ) {
    print "Value of a = $a\n";
} continue {
    $a = $a + 1;
}

my @list = ( 1, 2, 3, 4, 5 );
foreach $a (@list) {
    print "Value of a = $a\n";
} continue {
    last if $a == 4;
}
