#!/usr/bin/perl
use strict;
use warnings;

# bind replace
my $file_path = '/tmp/data.txt';
$file_path =~ s#/tmp#/var/tmp#;
print "$file_path\n";    # /var/tmp/data.txt
