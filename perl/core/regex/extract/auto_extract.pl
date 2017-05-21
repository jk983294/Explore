#!/usr/bin/perl
use strict;
use warnings;

my $str1 = "The food is in the salad bar";
$str1 =~ m/foo/;
print "Before: $`\n";     # 'The '
print "Matched: $&\n";    # 'foo'
print "After: $'\n";      # 'd is in the salad bar'


$str1 =~ m/foo/p;
print "Before: ${^PREMATCH}\n";    # 'The '
print "Matched: ${^MATCH}\n";      # 'foo'
print "After: ${^POSTMATCH}\n";    # 'd is in the salad bar'
