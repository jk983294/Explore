#!/usr/bin/perl
use strict;
use warnings;

# usage: perl word_count.pl ~/log

my %count;
my $total = 0;
my $valid = 0;

while (<>) {
    foreach (split) {
        $total++;
        next if /\W/;    # if not word, then continue
        $valid++;
        $count{$_}++;
    }
}

print "total is $total, valid is $valid\n";
while ( my ( $key, $value ) = each %count ) {
    print "$key => $value\n";
}
