#!/usr/bin/perl
use strict;
use warnings;
use File::Find;


my $path = '/home/kun/cpp/';

# find files end with cpp
sub wanted {
    if ( -f $File::Find::name ) {
        if ( $File::Find::name =~ /\.cpp$/ ) {
            print "$File::Find::name\n";
        }
    }
}

find( \&wanted, $path );
