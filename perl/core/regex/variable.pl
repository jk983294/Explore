#!/usr/bin/perl
use strict;
use warnings;

my $str1 = "The food is in the salad bar";
$str1 =~ m/foo/;
print "Before: $`\n";
print "Matched: $&\n";
print "After: $'\n";
