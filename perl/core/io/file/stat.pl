#!/usr/bin/perl
use strict;
use warnings;


my $file = "/tmp/file1.txt";
my @info = stat($file);
my ( $dev, $ino, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks ) = @info;

print "@info\n";
print "$dev, $ino, $nlink, $uid, $gid, $rdev, $size, $atime, $mtime, $ctime, $blksize, $blocks\n";

# lstat used for link file itself info
