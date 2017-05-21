#!/usr/bin/perl
use strict;
use warnings;

if ( !open CONFIG, '<:utf8', '/home/kun/data' ) {
    die "error $!";
}
if ( !open LOG, '>>:utf8', '/home/kun/log' ) {
    die "error $!";
}

select LOG;    # change print default output stream to LOG

while (<CONFIG>) {
    chomp;
    print $_;
}
