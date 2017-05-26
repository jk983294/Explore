#!/usr/bin/perl
use strict;
use warnings;

require "file1.pl";

MyUtils::hello();

my $foo = 5;
$::foo     = 21;
$main::foo = 22;

$MyUtils::foo = 43;

print( $foo, "\t", $MyUtils::foo, "\n" );
