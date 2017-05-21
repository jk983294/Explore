#!/usr/bin/perl
use strict;
use warnings;

# use pop/push as stack
sub add_remove {
    my @letters = ( "b", "c" );

    # add elements at the end of the array
    push( @letters, "d" );           # @letters  = b c d
    push( @letters, 'e' .. 'g' );    # @letters  = b c d e f g

    # add elements at the beginning of the array
    unshift( @letters, "a" );        # @letters  = a b c d e f g

    # remove one element from the last of the array.
    my $data = pop(@letters);        # @letters  = a b c d e f, $data = g

    # remove one element from the beginning of the array.
    $data = shift(@letters);         # @letters  = b c d e f, $data = a

    print "@letters\n";
}

sub slice {
    my @days      = qw/Mon Tue Wed Thu Fri Sat Sun/;
    my @weekdays  = @days[3, 4, 5];
    my @weekdays1 = @days[3 .. 5];
    print "@weekdays -- @weekdays\n";
}

# splice @ARRAY, OFFSET [ , LENGTH [ , LIST ] ]
sub splice_usage {
    my @nums = ( 0 .. 10 );

    # pop several elements
    my @deleted = splice( @nums, 8 );    # 8 9 10
    print "@deleted\n";
    @deleted = splice( @nums, 0, 2 );    # 0 1
    print "@deleted\n";

    # replace serveral elements
    splice( @nums, 1, 3, ( 11, 12, 13 ) );    # 2 11 12 13 6 7
    print "@nums\n";

    # insert without replace
    splice( @nums, 1, 0, ( 14, 15 ) );        # 2 14 15 11 12 13 6 7
    print "@nums\n";

}

sub get_length {
    my @nums    = ( 0 .. 20 );
    my @indexes = ( 0 .. $#nums );
    my $len     = $#indexes + 1;
    print "length is $len\n";
    print "Size: ", scalar @nums, "\n";       # physical size of the array, not the number of valid elements
    print "Max Index: ", $#nums, "\n";
}

sub reverse_usage {
    my @nums     = ( 0 .. 20 );
    my @reversed = reverse(@nums);
    print "reversed: @reversed\n";
    @nums = reverse(@nums);                   # reverse then save to original container
}

sub main {
    add_remove();
    slice();
    splice_usage();
    get_length();
    reverse_usage();
}

main();
