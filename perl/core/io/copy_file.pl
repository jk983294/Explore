#!/usr/bin/perl
use strict;
use warnings;

sub main {

    # Open file to read
    open( DATA1, "< /tmp/file1.txt" );

    # Open new file to write
    open( DATA2, "> /tmp/file2.txt" );

    # Copy data from one file to another.
    while (<DATA1>) {
        print DATA2 $_;
    }
    close(DATA1);
    close(DATA2);
}

main();
