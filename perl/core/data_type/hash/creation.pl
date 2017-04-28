#!/usr/bin/perl
use strict;
use warnings;

# the Hash variable will precede by sign % and will be used to store sets of key/value pairs.

sub main {
    my %data = ( 'John Paul', 45, 'Lisa', 30, 'Kumar', 40 );

    my %data1 = ();
    $data1{'John Paul'} = 45;
    $data1{'Lisa'}      = 30;
    $data1{'Kumar'}     = 40;

    my %data2 = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );

    my %data3 = ( -JohnPaul => 45, -Lisa => 30, -Kumar => 40 );

    my $hashref = {    # a reference to an anonymous hash
        'Adam'  => 'Eve',
        'Clyde' => 'Bonnie',
    };

    print "\$data{'John Paul'} = $data{'John Paul'}\n";
    print "\$data1{'Lisa'} = $data1{'Lisa'}\n";
    print "\$data2{'Kumar'} = $data2{'Kumar'}\n";
    print "\$data3{-JohnPaul} = " . $data3{-JohnPaul} . "\n";
}

main();
