#!/usr/bin/perl
use strict;
use warnings;

sub main {
    print "What is your name?\n";
    chomp( my $name = <STDIN> );    # remove last \n character
    print "Hello $name\n";

    while (<STDIN>) {               # ctrl+d finish input
        print "$_";
    }
}

main();
