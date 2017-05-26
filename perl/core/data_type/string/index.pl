#!/usr/bin/perl
use strict;
use warnings;

my $str = "hello world, kun!";
my $where = index( $str, 'world' );
print "$where\n";    # 6

$where = index( $str, 'morld' );
print "$where\n";    # -1

$where = index( $str, 'l' );                # first l
$where = index( $str, 'l', $where + 1 );    # next l
$where = index( $str, 'l', $where + 1 );    # third l
print "$where\n";                           # 9

# reverse search
$where = rindex( $str, 'l' );               # last l
$where = rindex( $str, 'l', $where - 1 );   # previous l
$where = rindex( $str, 'l', $where - 1 );   # first l
print "$where\n";                           # 2
