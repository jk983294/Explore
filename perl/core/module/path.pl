#!/usr/bin/perl
use strict;
use warnings;
use Path::Class;

my $dir         = dir(qw(usr local bin));
my $subdir      = $dir->subdir('perl');
my $parent      = $dir->parent;
my $windows_dir = $dir->as_foreign('Win32');
print "$dir $subdir $parent $windows_dir\n";    # usr/local/bin usr/local/bin/perl usr/local usr\local\bin
