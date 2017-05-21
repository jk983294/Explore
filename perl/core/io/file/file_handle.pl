#!/usr/bin/perl
use strict;
use warnings;

if ( !open CONFIG, '<:utf8', '/home/kun/data' ) {
    die "error $!";
}
if ( !open LOG, '>>:utf8', '/home/kun/log' ) {
    die "error $!";
}

while (<CONFIG>) {
    print LOG $_;
}

# use variable instead of bareword
open my $config_fh, '<:utf8',  '/home/kun/data' or die "error $!";
open my $log_fh,    '>>:utf8', '/home/kun/log'  or die "error $!";

while (<$config_fh>) {
    print $log_fh $_;
}
