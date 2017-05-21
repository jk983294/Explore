#!/usr/bin/perl
use strict;
use warnings;

# good example: hostname <==> ip address
my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );
my %inversed = reverse %data;
print "$inversed{45}\n";    # John Paul
