#!/usr/bin/perl
use strict;
use warnings;


my %scores = ( "b" => 195, "f" => 205, "d" => 30, "a" => 195 );

sub by_score_name {
    ( $scores{$b} <=> $scores{$a} ) or ( $a cmp $b );
}
my @winners = sort by_score_name keys %scores;
print "@winners\n";    # f a b d
