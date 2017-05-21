#!/usr/bin/perl
use strict;
use warnings;

$_ = '  hello    there,   kun   ';
s/\s+/ /g;         # condense to one space
s/^\s+|\s+$//g;    # remove head and tail space
print "$_\n";      # hello there, kun

s/KUN/jk/gi;
print "$_\n";      # hello there, jk
