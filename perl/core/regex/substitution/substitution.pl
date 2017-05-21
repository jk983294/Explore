#!/usr/bin/perl
use strict;
use warnings;

$_ = 'hello there, kun';
s/kun/jk/;
print "$_\n";    # hello there, jk

if (s/(\w+) (\w+)/$2 $1/) {
    print "replace success, $_\n";    # there hello, jk
}
