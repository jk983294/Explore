#!/usr/bin/perl
use strict;
use warnings;

my $str = "hello world, kun!";
my $found = substr( $str, 6, 5 );
print "$found\n";    # world

# get sub string till end
$found = substr( $str, 6 );
print "$found\n";    # world, kun!

# change sub string
substr( $str, 0, 5 ) = "Goodbye";
print "$str\n";      # Goodbye world, kun!
