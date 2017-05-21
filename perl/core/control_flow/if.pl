#!/usr/bin/perl
use strict;
use warnings;

my $a = 100;
if ( $a == 20 ) {
    printf "a has a value which is 20\n";
} elsif ( $a == 30 ) {
    printf "a has a value which is 30\n";
} else {
    printf "a has a value which is $a\n";
}

print "$a is positive number\n" if $a > 0;

$a = '0';
if ( !$a ) {
    print "\'0\' is false\n";
}
$a = 0;
if ( !$a ) {
    print "0 is false\n";
}

# convert to bool
my $still_true  = !!'jk';
my $still_false = !!'0';
