#!/usr/bin/perl
use strict;
use warnings;

sub main {

    # concatenate
    my $num  = 42;
    my $str  = "hello" . "world";
    my $str1 = "hello" . "world" . "\n";
    my $mix  = $str . $num;

    # repeatition
    print "a" x 3 . "\n";    # aaa
    print 5 x 3 . "\n";      # 555
    print 5 x 3.5 . "\n";    # 555
    print 5 x 0 . "\n";      # ""

    # conversion
    print "2" * "3";         # 6
    print "Z" . 5 * 7;       # Z35

    print( length($str),  "\n" );    # 10
    print( uc($str),      "\n" );    # HELLOWORLD
    print( lc($str),      "\n" );    # helloworld
    print( ucfirst($str), "\n" );    # Helloworld
    print( lcfirst($str), "\n" );    # helloworld
}

main();
