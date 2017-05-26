#!/usr/bin/perl
use strict;
use warnings;

sub divide {
    my ( $a, $b ) = @_;
    my $result = eval { $a / $b };
    return $result;
}

print( divide( 1, 2 ), "\n" );
print( divide( 2, 0 ), "\n" );
print( divide( 6, 5 ), "\n" );
