#!/usr/bin/perl
use strict;
use warnings;

foreach (qw(a b c ab bc ac abc)) {
    if (/^a/) {
        print "matched, string is $_\n";
    }
}
