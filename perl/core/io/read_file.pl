#!/usr/bin/perl
use strict;
use warnings;

sub main {
    open( DATA, "< /tmp/file1.txt" ) or die "Can't open data";
    my @lines = <DATA>;
    print "@lines";
    close(DATA);
}

main();
