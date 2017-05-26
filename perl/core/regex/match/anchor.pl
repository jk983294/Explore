#!/usr/bin/perl
use strict;
use warnings;

my $str = 'foobarbarfoo';

$str =~ /bar(?=bar)/;    # "bar" which has "bar" after it
print "|$`|$&|$'|\n";    # |foo|bar|barfoo|

$str =~ /bar(?=bar)/;    # "bar" which does not have "bar" after it
print "|$`|$&|$'|\n";    # |foo|bar|barfoo|

$str =~ /(?<=foo)bar/;   # "bar" which has "foo" before it
print "|$`|$&|$'|\n";    # |foo|bar|barfoo|

$str =~ /(?<!foo)bar/;   # "bar" which does not have "foo" before it
print "|$`|$&|$'|\n";    # |foobar|bar|foo|

$str =~ /(?<=foo)bar(?=bar)/;    # "bar" with "foo" before it and "bar" after it
print "|$`|$&|$'|\n";            # |foo|bar|barfoo|

# puzzle: find words that have the first 5 letters of alphabet in consecutive order
my @words = qw(bedcap bedcase biofeedback dfgksdfg brocade);

foreach (@words) {
    if (
        /
        ([abcde])(?!\1) # first char, not the same char follow
        ([abcde])(?!\1|\2) # any char except \1 and \2
        ([abcde])(?!\1|\2|\3) # any char except \1, \2 and \3
        ([abcde])(?!\1|\2|\3|\4) # any char except \1, \2, \3 and \4
        ([abcde])
    /x
        )
    {
        print "$_\n";
    }
}
