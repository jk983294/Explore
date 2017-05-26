#!/usr/bin/perl
use strict;
use warnings;

my $count = unlink glob '*.o';
print "delete $count files\n";
