#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my @ages = ( 25, 30, 40 );
    my @var_abc = ( 'a' .. 'z' );    # .. range operator

    print "\$ages[0] = $ages[0]\n";
    print "\$var_abc[0] = $var_abc[0]\n";
    print "\$var_abc[-1] = $var_abc[-1]\n";

    # Selecting Elements from Lists
    my $var  = ( 5, 4, 3, 2, 1 )[4];
    my @list = ( 5, 4, 3, 2, 1 )[ 1 .. 3 ];
}

main();
