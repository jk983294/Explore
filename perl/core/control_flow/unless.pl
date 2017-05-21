#!/usr/bin/perl
use strict;
use warnings;

# unless do the opposite check of if

my $a = 40;
unless ( $a > 30 ) {
    printf "a has a value which is not greater than 30\n";
} elsif ( $a < 20 ) {
    printf "a has a value which is not less than 20\n";
} else {
    printf "a has a value which is $a\n";
}

print "a has a value which is not 20" unless $a == 30;
