#!/usr/bin/perl
use strict;
use warnings;

# @ARGV     array contain command line arguments
# ARGV      file handler providing filter behaviour (used as default file handle for <>)
# $ARGV     name of file being read through ARGV file handler
# $#ARGV    size

# usage: perl argv.pl env.pl pipe.pl

my $total_lines = 0;
my $total_bytes = 0;
my %lines       = ();
my %bytes       = ();
for my $file (@ARGV) {
    $lines{$file} = 0;
    $bytes{$file} = 0;
}

while (<>) {
    $lines{$ARGV}++;
    $bytes{$ARGV} += length($_);
    $total_lines++;
    $total_bytes += length($_);
}

my @names = keys %lines;
for my $file (@names) {
    print "$lines{$file}\t$bytes{$file}\t$file\n";
}

if ($#names) {
    print "$total_lines\t$total_bytes\ttotal\n";
}
