#!/usr/bin/perl
use strict;
use warnings;

sub my_func {
    my ( $a, $b, $opt ) = @_;    # copy for defensive programming
    print "$a\t$b\t$opt\n";
}

my_func( 1, 2 );
my_func( 1, 2, 3 );
