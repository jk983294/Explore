#!/usr/bin/perl
use strict;
use warnings;

my $dir = "/tmp/*";    # Display all the files in /tmp directory.
$dir = "/tmp/*.c";          # Display all the C source files in /tmp directory.
$dir = "/tmp/.*";           # Display all the hidden files.
$dir = "/tmp/* /home/*";    # Display all the files from /tmp and /home directories.
my @files = glob($dir);     # get all files and sort by file name

foreach (@files) {
    print "$_\n";
}

# another syntax of glob
@files = </tmp/* /home/*>;    # this is not read from file handler
foreach (@files) {
    print "$_\n";
}
