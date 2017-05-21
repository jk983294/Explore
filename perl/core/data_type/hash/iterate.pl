#!/usr/bin/perl
use strict;
use warnings;

my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );

while ( my ( $key, $value ) = each %data ) {
    print "$key => $value\n";
}

# iterate by key order
foreach my $key ( sort keys %data ) {
    print "$key => $data{$key}\n";
}
