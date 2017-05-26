#!/usr/bin/perl
use strict;
use warnings;
use Cwd;

my $pwd = cwd();    #-- get current directory

my $dir = "/tmp";
chdir($dir) or die "Couldn't go inside $dir directory, $!";
print "Your new location is $dir\n";


chdir() or die "Couldn't go home directory, $!";    # no arg means go to user home dir
$pwd = cwd();
print "Your new location is $pwd\n";
