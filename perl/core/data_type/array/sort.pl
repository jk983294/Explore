#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my @foods = qw(pizza steak chicken burgers);
    print "Before: @foods\n";

    # sort this array based on ASCII Numeric value of the words
    @foods = sort(@foods);
    print "After: @foods\n";
}

main();
