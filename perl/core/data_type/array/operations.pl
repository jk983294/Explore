#!/usr/bin/perl
use strict;
use warnings;

sub add_remove {
    my @coins = ( "Quarter", "Dime", "Nickel" );

    # add one element at the end of the array
    push( @coins, "Penny" );    # @coins  = Quarter Dime Nickel Penny

    # add one element at the beginning of the array
    unshift( @coins, "Dollar" );    # @coins  = Dollar Quarter Dime Nickel Penny

    # remove one element from the last of the array.
    pop(@coins);                    # @coins  = Dollar Quarter Dime Nickel

    # remove one element from the beginning of the array.
    shift(@coins);                  # @coins  = Quarter Dime Nickel
}

sub slice {
    my @days      = qw/Mon Tue Wed Thu Fri Sat Sun/;
    my @weekdays  = @days[3, 4, 5];
    my @weekdays1 = @days[3 .. 5];
    print "@weekdays -- @weekdays\n";
}

sub replace {
    my @nums = ( 1 .. 20 );
    print "Before - @nums\n";

    # splice @ARRAY, OFFSET [ , LENGTH [ , LIST ] ]
    splice( @nums, 5, 5, 21 .. 25 );
    print "After - @nums\n";
}

sub main {
    my @var_abc = ( 'a' .. 'z' );    # .. range operator

    print "Size: ", scalar @var_abc, "\n";    # physical size of the array, not the number of valid elements
    print "Max Index: ", $#var_abc, "\n";

    add_remove();
    slice();
    replace();
}

main();
