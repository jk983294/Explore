#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my $a = 10;
    print "Value of a = $a\n";
    print 'Value of a = $a\n';    # single quote does not interpolate any variable or special character
    print '\\\'';                 # only \ and ' need interpolate in single quote

    my $book  = 'book';
    my $books = 'books';
    print "${book}ss";            # bookss
}

main();
