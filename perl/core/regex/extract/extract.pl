#!/usr/bin/perl
use strict;
use warnings;

my $time = "10:10:10";
my ( $hours, $minutes, $seconds ) = ( $time =~ m/(\d+):(\d+):(\d+)/ );
print "$hours, $minutes, $seconds\n";

# group extracted variable saved in $n
if ( $time =~ /(\d+):(\d+):(\d+)/ ) {
    print "$1, $2, $3\n";
}

if ( 'hello there, kun' =~ /(\S+)\s(\S+),\s(\S+)/ ) {
    print "$1, $2, $3\n";    # hello, there, kun
}
