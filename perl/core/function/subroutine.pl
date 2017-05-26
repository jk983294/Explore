#!/usr/bin/perl
use strict;
use warnings;

# arguments lives in @_, first argument to the function is in $_[0]
sub average {
    my $n   = scalar(@_);    # get total number of arguments passed.
    my $sum = 0;

    foreach my $item (@_) {
        $sum += $item;
    }
    my $average = $sum / $n;
    return $average;
}

# Passing Lists to Subroutines, make list as the last argument
sub PrintList {
    my @list = @_;           # [10 1 2 3 4]
    print "Given list is @list\n";
}

# Passing Hashes to Subroutines, hash is automatically translated into a list of key/value pairs
sub PrintHash {
    my (%hash) = @_;

    foreach my $key ( keys %hash ) {
        my $value = $hash{$key};
        print "$key : $value\n";
    }
}

sub say_hello {
    print "hello\n";
}

sub max {
    my $max_so_far = shift @_;
    foreach (@_) {
        if ( $_ > $max_so_far ) {
            $max_so_far = $_;
        }
    }
    $max_so_far;
}

sub index_of {
    my ( $what, @data ) = @_;
    foreach ( 0 .. $#data ) {
        if ( $what eq $data[$_] ) {
            return $_;
        }
    }
    return -1;
}

sub main {
    &say_hello;

    print max( 1, 2, 3 ), "\n";
    print index_of( 'b', ( 'a' .. 'z' ) ), "\n";

    my $num = average( 10, 20, 30 );
    print "Average for the given numbers : $num\n";

    my $a = 10;
    my @b = ( 1, 2, 3, 4 );
    PrintList( $a, @b );

    my %hash = ( 'name' => 'Tom', 'age' => 19 );
    PrintHash(%hash);
}

main();
