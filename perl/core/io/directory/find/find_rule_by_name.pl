#!/usr/bin/perl
use strict;
use warnings;
use File::Find::Rule;

my $path = '/home/kun/cpp/';

my @files = File::Find::Rule->file()->name('*.cpp')->in($path);

foreach (@files) {
    print "$_\n";
}
