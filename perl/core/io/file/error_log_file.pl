#!/usr/bin/perl
use strict;
use warnings;

if ( !open STDERR, '>>/home/kun/elog' ) {
    die "error $!";
}

while (<>) {
    print STDERR $_;
}
