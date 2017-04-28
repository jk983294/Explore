#!/usr/bin/perl
use strict;
use warnings;

# A scalar variable will precede by sign $ and it can store either a number, a string, or a reference.

sub main {
    my $var_integer             = 1234;
    my $var_negative_integer    = -100;
    my $var_floating_point      = 200.0;
    my $var_scientific_notation = 16.12E14;
    my $var_hexadecimal         = 0xffff;
    my $var_octal               = 0577;
    my $name                    = "John Paul";

    print "var_integer = $var_integer\n";
    print "var_scientific_notation = $var_scientific_notation\n";
    print "Name = $name\n";
}

main();
