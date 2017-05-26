#!/usr/bin/perl
use strict;
use warnings;

sub my_func {
    my %default_value = ( 'a' => 1, 'b' => 2, 'c' => 3 );
    my %args = ( %default_value, @_ );
    print "$args{a}\t$args{b}\t$args{c}\n";
}

my_func();
my_func( 'a' => 2 );
my_func( 'a' => 3, 'b' => 2, 'c' => 1 );
