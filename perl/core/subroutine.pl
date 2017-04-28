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

sub main {
    my $num = average( 10, 20, 30 );
    print "Average for the given numbers : $num\n";

    my $a = 10;
    my @b = ( 1, 2, 3, 4 );
    PrintList( $a, @b );

    my %hash = ( 'name' => 'Tom', 'age' => 19 );
    PrintHash(%hash);
}

main();
