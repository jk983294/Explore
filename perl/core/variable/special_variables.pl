#!/usr/bin/perl
use strict;
use warnings;

sub main {
    foreach ( 'hickory', 'dickory', 'doc' ) {
        print $_;
        print "\n";
    }

    foreach ( 'hickory', 'dickory', 'doc' ) {
        print;
        print "\n";
    }
}

main();
