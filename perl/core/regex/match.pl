#!/usr/bin/perl
use strict;
use warnings;

my $bar = "This is foo and again foo";
if ( $bar =~ /foo/ ) {
    print "matching\n";
}

if ( $bar =~ m[foo] ) {
    print "matching\n";
}

if ( $bar =~ m{foo} ) {
    print "matching\n";
}

if ( $bar !~ m{fooo} ) {
    print "not matching\n";
}

my $isFoo = ( $bar =~ m/foo/ );
print "$isFoo"
