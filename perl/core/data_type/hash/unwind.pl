#!/usr/bin/perl
use strict;
use warnings;

my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );
my @array = %data;
print "Array : @array\n";    # Array : Kumar 40 Lisa 30 John Paul 45
