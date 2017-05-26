#!/usr/bin/perl
use strict;
use warnings;

opendir( my $dh, '/tmp/' ) or die "Couldn't open directory, $!";
while ( my $file = readdir $dh ) {
    next if ( $file eq "." or $file eq ".." );
    print "$file\n";
}
closedir $dh;

# print the list of C source files
print "\n";
opendir( DIR, '/tmp/' ) or die "Couldn't open directory, $!";
foreach ( sort grep( /^.*\.c$/, readdir(DIR) ) ) {
    print "$_\n";
}
closedir DIR;
