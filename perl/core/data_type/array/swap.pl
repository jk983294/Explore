#!/usr/bin/perl
use strict;
use warnings;

( my $a, my $b ) = ( "a", "b" );
( $a, $b ) = ( $b, $a );

print "$a <--> $b\n";
