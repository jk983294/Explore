#!/usr/bin/perl
use strict;
use warnings;

my %h1 = ( "a" => 1, "b" => 2 );
my %h2 = ( "a" => 3, "b" => 1 );
my @a1 = qw( a b c d );
my @a2 = qw( a b c d );
my $v1 = 'abc';
my $v3;

print( %h1  ~~ %h2,       "\n" );    # true, check key of hash is the same
print( %h1  ~~ @a1,       "\n" );    # true, at least one hash key is in array
print( %h1  ~~ /a/,       "\n" );    # true, at least one hash key match regex
print( 'a'  ~~ %h1,       "\n" );    # true, hash contains key 'a'
print( @a1  ~~ @a2,       "\n" );    # true, the same array
print( @a1  ~~ /a/,       "\n" );    # true, at least one element in array match regex
print( $v3  ~~ undef $v3, "\n" );    # true, variable undefined
print( $v1  ~~ /a/,       "\n" );    # true, variable match regex
print( 123  ~~ ' 123.0',  "\n" );    # true, numish variable equal
print( 'jk' ~~ 'jk',      "\n" );    # true, string equal
print( 123  ~~ 123,       "\n" );    # true, number equal
