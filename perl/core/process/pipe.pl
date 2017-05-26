#!/usr/bin/perl
use strict;
use warnings;

# pipe will create a new perl process

open my $date, 'date |' or die "cannot pipe from date: $!";
while (<$date>) {
    print;
}
close $date;

# find files access time > 90 dyas, size > 1000 bytes
open my $find_fh, '-|', 'find', qw( /bin/ -atime +90 -size +1000 -print) or die "fork: $!";
while (<$find_fh>) {
    chomp;
    printf "%s size %dK last access %.2f days ago.\n", $_, ( 1023 + -s $_ ) / 1024, -A $_;
}

open my $cat, '| cat' or die "cannot pipe to echo: $!";
print $cat "hello world.";
close $cat;
