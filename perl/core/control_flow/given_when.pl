#!/usr/bin/perl
use strict;
use warnings;
use 5.022;

my $data = 'jk';
given ($data) {
    when ( $_ eq 'jk' ) { say "jk"; }    # default break if no explicity continue
    when ( $_ =~ /kun/ ) { say "find regex kun"; continue; }
    when ( !/jiang/i ) { say "not jiang"; }    # all negative check is not smart match
    when ('42')        { say "number $_"; }    # default is smart match
    default            { say "no idea."; }
}

my @a = qw( jk jiang kun 42 52 );
given (@a) {                                   # array check
    when ( $_ eq 'jk' ) { say "jk"; }
    when ( $_ =~ /kun/ ) { say "find regex kun"; continue; }
    when ( !/jiang/i )   { say "not jiang"; }
    when ('42')          { say "number $_"; }
    default              { say "no idea."; }
}
