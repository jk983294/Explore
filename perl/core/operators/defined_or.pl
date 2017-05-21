#!/usr/bin/perl
use strict;
use warnings;

my $verbose = $ENV{VERBOSE} // 1;    # if not define, use 1
print "$verbose\n" if $verbose;

foreach my $try ( 0, undef, '0', 1, 42 ) {
    my $value = $try // 'default';
    print "$value\n";
}
