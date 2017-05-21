#!/usr/bin/perl
use strict;
use warnings;

$_ = 'jkabbajk';
if (/(.)(.)\2\1/) {    # match abba
    print "matched, string is $_\n";
}
if (/(.)(.)\g{2}\g{1}/) {    # in case \1 against \11
    print "matched, string is $_\n";
}
