#!/usr/bin/perl
use strict;
use warnings;

my ( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst ) = localtime();
my $dt = sprintf( "%4d%02d%02d %02d:%02d:%02d", $year + 1900, $mon + 1, $mday, $hour, $min, $sec );
print "$dt\n";    # 20170523 21:27:52

my $money = sprintf( "%.2f", 2.49999 );
print "$money\n";    # 2.50

sub big_number {
    my $num = sprintf( "%.2f", shift @_ );
    'keep loop' while $num =~ s/^(-?\d+)(\d\d\d)/$1,$2/;
    $num =~ s/^(-?)/$1\$/;
    return $num;
}

print big_number(3212344237.3423),  "\n";    # $3,212,344,237.34
print big_number(-3212344237.3423), "\n";    # -$3,212,344,237.34
