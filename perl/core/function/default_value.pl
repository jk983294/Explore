#!/usr/bin/perl
use strict;
use warnings;

sub my_func {
    my $value = shift @_ || "default";
    return $value;
}

print( my_func(),        "\n" );
print( my_func("value"), "\n" );
