#!/usr/bin/perl
use strict;
use warnings;

if ( 'foo' =~ /\w+/ ) {
    print "matching\n";
}

if ( '123' =~ m[\d+] ) {
    print "matching\n";
}

if ( " \t " =~ m{\s+} ) {
    print "matching\n";
}

if ( 'foo' !~ /\W+/ ) {
    print "not matching\n";
}

if ( '123' !~ m[\D+] ) {
    print "not matching\n";
}

if ( " \t " !~ m{\S+} ) {
    print "not matching\n";
}
