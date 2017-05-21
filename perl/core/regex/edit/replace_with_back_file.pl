#!/usr/bin/perl
use strict;
use warnings;

# usgae: perl replace.pl ~/log
# this variable means save back file, then edit original file.
# if $^I = "", then no back file created, just edit original file.
$^I = ".bak";

while (<>) {
    s/jk/kun/gi;
    print;
}
