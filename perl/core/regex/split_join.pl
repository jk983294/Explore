#!/usr/bin/perl
use strict;
use warnings;

my @fields = split /:/, "abc:def::g:h";
print "@fields\n";    # 'abc' 'def' '' 'g' 'h'
print( ( join ':', @fields ), "\n" );

my @data = split /\s+/, "   this  is my day.  ";
print "@data\n";      # '' 'this' 'is' 'my' 'day.'
print( ( join ' ', @data ), "\n" );

$_ = "   this  is my day.  ";
my @data1 = split;    # remove head space
print "@data1\n";     # 'this' 'is' 'my' 'day.'
print( ( join ' ', @data1 ), "\n" );

print( ( join '-', 1, 2, 3, 4, 5 ), "\n" );    # 1-2-3-4-5
