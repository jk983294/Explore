#!/usr/bin/perl
use strict;
use warnings;

# undef behave as 0 and ''

sub main {
    my $sum += 2;
    my $str .= "my str";
    print "$str $sum\n";
    $sum = undef;
    if ( defined($sum) ) {
        print '$sum is defined' . "\n";
    } else {
        print '$sum is undefined' . "\n";
    }
}

main();
