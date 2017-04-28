#!/usr/bin/perl
use strict;
use warnings;

sub main {
    print "What is your name?\n";
    my $name = <STDIN>;
    print "Hello $name\n";
}

main();
