#!/usr/bin/perl
use strict;
use warnings;

if ( 'foo' =~ /FOO/i ) {    # ignore case
    print "matching\n";
}

if ( "123\n123" =~ /123.123/s ) {    # default . not match \n
    print "matching\n";
}

if ( "123abc123" =~ / \d+ \w+ \d+ /x ) {    # ignore space
    print "matching\n";
}

# boundary
if ( "123abc123" !~ /\babc\b/ ) {
    print "not matching\n";
}

if ( "123 abc 123" =~ /\babc\b/ ) {
    print "matching\n";
}

# charset
if ( 'foo' =~ /\w+/a ) {    # ASCII
    print "matching\n";
}
if ( 'foo' =~ /\w/u ) {     # unicode
    print "matching\n";
}
if ( 'foo' =~ /\w/l ) {     # locale
    print "matching\n";
}
