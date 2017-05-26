#!/usr/bin/perl
use strict;
use warnings;


my @strings = qw( aa z A Fsdf k V j );

my @sorted = sort { $a cmp $b } @strings;
print "@sorted\n";    # A Fsdf V aa j k z

@sorted = sort { $b cmp $a } @strings;
print "@sorted\n";    # z k j aa V Fsdf A

# sort ingore case
@sorted = sort { lc $a cmp lc $b } @strings;
print "@sorted\n";    # A aa Fsdf j k V z

# sort based on length
@sorted = sort { length $a cmp length $b } @strings;
print "@sorted\n";    # z A k V j aa Fsdf
