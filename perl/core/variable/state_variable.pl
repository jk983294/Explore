#!/usr/bin/perl
use strict;
use warnings;
use feature 'state';

# another type of lexical variables, which are similar to private variables
# but they maintain their state and they do not get reinitialized upon multiple calls of the subroutines.
# C++ static variable in function

sub PrintCount {
    state $count = 0;    # initial value
    print "Value of counter is $count\n";
    $count++;
}

# Prior to Perl 5.10, you would have to write it like this, use closure
{
    my $count = 0;       # initial value

    sub PrintCount1 {
        print "Value of counter is $count\n";
        $count++;
    }
}

sub main {
    for ( 1 .. 5 ) {
        PrintCount();
    }

    for ( 1 .. 5 ) {
        PrintCount1();
    }
}

main();
