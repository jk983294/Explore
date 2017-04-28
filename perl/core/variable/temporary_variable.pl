#!/usr/bin/perl
use warnings;

# A local just gives temporary values to global (meaning package) variables. This is known as dynamic scoping
# This operator works by saving the current values of those variables in its argument list on a hidden stack
# and restoring them upon exiting the block, subroutine, or eval.

sub PrintHello {
    local $string;
    $string = "Hello, Perl!";
    PrintMe();
    print "Inside the function PrintHello $string\n";
}

sub PrintMe {
    print "Inside the function PrintMe $string\n";
}

sub main {
    $string = "Hello, World!";    # Global variable
    PrintHello();
    print "Outside the function $string\n";
}

main();
