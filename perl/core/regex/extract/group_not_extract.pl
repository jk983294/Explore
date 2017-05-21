#!/usr/bin/perl
use strict;
use warnings;

if ( 'hello there, kun' =~ /(\S+)\s(\S+),\s(\S+)/ ) {
    print "$1, $2, $3\n";    # hello, there, kun
}

# ?: not capture
if ( 'hello there, kun' =~ /(?:\S+)\s(\S+),\s(\S+)/ ) {
    print "$1, $2\n";        # there, kun
}
