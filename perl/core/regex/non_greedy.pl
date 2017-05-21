#!/usr/bin/perl
use strict;
use warnings;

# non-greedy version: +? *? {5,10}? {5,}? ??

my $html = 'hello <BOLD>there</BOLD>, <BOLD>kun</BOLD>';
$html =~ s#<BOLD>(.*?)</BOLD>#$1#g;
print "$html\n";
