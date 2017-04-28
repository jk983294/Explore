#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my @foods = qw(pizza steak chicken burgers);

    # Perl arrays have zero-based indexing, $[ will almost always be 0.
    # But if you set $[ to 1 then all your arrays will use one-based indexing.
    $[ = 1;

    print "Food at \@foods[1]: $foods[1]\n";
    print "Food at \@foods[2]: $foods[2]\n";
}

main();
