#!/usr/bin/perl
use strict;
use warnings;

my $a = '23a';
my $b = 'c12';

if ( '123abc123' =~ /($a).*($b)/ ) {    # /(23a).*(c12)/
    print "matching\n";
}
