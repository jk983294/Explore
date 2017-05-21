#!/usr/bin/perl
use strict;
use warnings;

my @nums = ( 1 .. 3 );

foreach my $i (@nums) {
    print "$i\n";
}

foreach (@nums) {
    print "$_\n";
}

# iterate with index
while ( my ( $index, $value ) = each @nums ) {
    print "$index : $value\n";
}

foreach my $index ( 0 .. $#nums ) {
    print "$index : $nums[$index]\n";
}
