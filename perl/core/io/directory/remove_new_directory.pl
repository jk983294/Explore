#!/usr/bin/perl
use strict;
use warnings;

my $dir = "/tmp/perl";
rmdir($dir) or die "Couldn't remove $dir directory, $!";
print "Directory removed successfully\n";
