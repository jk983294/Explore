#!/usr/bin/perl
use strict;
use warnings;

package MyUtils;    # namespace

sub hello {
    print "hello.\n";
}

our $foo = 42;

1;                  # file should end with true expression
