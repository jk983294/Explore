#!/usr/bin/perl
use strict;
use warnings;

sub check_exists {
    my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );

    print "contains: " . exists( $data{'Lisa'} ) . "\n";     # contains: 1
    print "contains: " . exists( $data{'Lisa1'} ) . "\n";    # contains:
    print "contains: " . $data{'Lisa'} . "\n";               # contains: 30
    print "contains: "
      . $data{'Lisa1'}
      . "\n";    # contains: ; $data{'Lisa1'} = undefined
}

sub get_size {
    my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );
    my $size = keys %data;
    print "Hash size: $size\n";
    $size = values %data;
    print "Hash size: $size\n";
}

sub add_remove {
    my %data = ( 'John Paul' => 45, 'Lisa' => 30, 'Kumar' => 40 );
    $data{'Ali'} = 55;      # adding an element to the hash;
    delete $data{'Ali'};    # delete the same element from the hash;
    print "%data\n";
}

sub main {
    check_exists();
    get_size();
    add_remove();
}

main();
