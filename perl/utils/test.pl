#!/usr/bin/perl
use strict;
use warnings;

require "TimeUtils.pl";
require "StringUtils.pl";

print( TimeUtils::date(),         "\n" );    # 20170908
print( TimeUtils::getfancytime(), "\n" );    # 20:11:54
print( TimeUtils::get_gmttime(),  "\n" );    # 20170908.201154

print( StringUtils::trim(' hello world '),     "\n" );
print( StringUtils::trim(' hello world     '), "\n" );
print( StringUtils::trim('    hello world '),  "\n" );

print( StringUtils::reverseCase('hello WORLD'), "\n" );
