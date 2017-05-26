#!/usr/bin/perl
use strict;
use warnings;

# use grep to select elements
my @nums = ( 1 .. 10 );
my @odd_nums = grep { $_ % 2 } @nums;
print "@odd_nums\n";

open my $fh, "< /tmp/file1.txt" or die "Can't open $!";
my @matched_lines = grep {/jk/i} <$fh>;
print "@matched_lines\n";
close $fh;
