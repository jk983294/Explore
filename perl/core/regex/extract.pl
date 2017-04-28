#!/usr/bin/perl
use strict;
use warnings;

my $time = "10:10:10";
my ( $hours, $minutes, $seconds ) = ( $time =~ m/(\d+):(\d+):(\d+)/ );
print "$hours, $minutes, $seconds"
