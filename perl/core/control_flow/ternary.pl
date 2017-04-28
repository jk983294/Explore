#!/usr/bin/perl
use strict;
use warnings;

my $age = 10;
my $status = ($age > 60 )? "A senior citizen" : "Not a senior citizen";
printf "$age\n$status\n"
