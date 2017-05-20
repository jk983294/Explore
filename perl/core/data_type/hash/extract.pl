#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );
    my @array = @data{'Lisa', 'Kumar'};    # extract some values
    print "Array : @array\n";              # Array : 30 40

    my @names = keys %data;                # extract keys
    my @ages  = values %data;              # extract values
}

main();
