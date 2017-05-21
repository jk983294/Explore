#!/usr/bin/perl
use strict;
use warnings;

# copy replace
my $file_path = '/tmp/data.txt';
( my $copy = $file_path ) =~ s#/tmp#/var/tmp#;
print "$file_path $copy\n";    # /tmp/data.txt /var/tmp/data.txt
