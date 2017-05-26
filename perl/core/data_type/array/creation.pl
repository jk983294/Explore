#!/usr/bin/perl
use strict;
use warnings;

# An array variable will precede by sign @ and it will store ordered lists of scalars.

sub main {
    my @ages = ( 25, 30, 40 );
    @ages[3, 4] = ( 50, 60 );
    print "@ages\n";    # 25 30 40 50 60

    my @names = ( "John Paul", "Lisa", "Kumar" );
    my @array = ( 1,           2,      'Hello' );

    # quoted word, taken as '', save lots of quote writes
    my @qw_array = qw(This is an array);     # returns a list of strings, separating the delimited string by white space
    my @days     = qw(one two three four);
    my @files    = qw {
        /usr/local/lib/system.so
        /home/jk/note.txt
    };

    my @var_10  = ( 1 .. 10 );               # Sequential Number Arrays
    my @var_abc = ( 'a' .. 'z' );            # .. range operator

    my $arrayref = [1, 2, ['a', 'b', 'c']];  # a reference to an anonymous array

    # merged array
    my @odd  = ( 1, 3, 5 );
    my @even = ( 2, 4, 6 );
    my @numbers = ( @odd, @even );           # 1 3 5 2 4 6

    print "@var_abc\n";
}

main();
