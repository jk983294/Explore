#!/usr/bin/perl
use strict;
use warnings;

sub main {
    print "File name " . __FILE__ . "\n";
    print "Line Number " . __LINE__ . "\n";
    print "Package " . __PACKAGE__ . "\n";

    # they can not be interpolated
    print "__FILE__ __LINE__ __PACKAGE__\n";
}

main();
