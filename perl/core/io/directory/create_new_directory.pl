#!/usr/bin/perl
use strict;
use warnings;

my $dir = "/tmp/perl";
mkdir($dir) or die "Couldn't create $dir directory, $!";
print "Directory created successfully\n";
