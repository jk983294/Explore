#!/usr/bin/perl
#use strict;
use warnings;

# By default, all variables in Perl are global variables
# create private variables called lexical variables at any time with the my operator.
# A local just gives temporary values to global (meaning package) variables. This is known as dynamic scoping

sub PrintHello {
    my $string;    # Private variable for PrintHello function
    my ( $another, @an_array, %a_hash );    # declaring many variables at once
    $string = "Hello, Perl!";
    print "Inside the function $string\n";
}

sub main {
    $string = "Hello, World!";              # Global variable
    PrintHello();
    print "Outside the function $string\n";
}

main();
