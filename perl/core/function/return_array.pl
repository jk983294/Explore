#!/usr/bin/perl
use strict;
use warnings;

sub my_func {
    my @a = qw(a b c);
    return @a;
}

my $x = my_func();
my @y = my_func();

print "$x\n";    # 3
print "@y\n";    # a b c
