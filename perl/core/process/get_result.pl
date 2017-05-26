#!/usr/bin/perl
use strict;
use warnings;

chomp( my $now = `date` );
print "now: $now\n";

my $output = qx'echo $$';
print "$output\n";

my @functions = qw( int sleep length);
my %about     = ();
foreach (@functions) {
    $about{$_} = qx(perldoc -t -f $_);
}

foreach (`who`) {
    my ( $user, $tty, $date ) = /(\S+)\s+(\S+)\s+(.*)/;
    print "$user is in $tty at $date\n";
}
