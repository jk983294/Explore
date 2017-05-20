#!/usr/bin/perl
use strict;
use warnings;

# The redo command restarts the loop block without evaluating the conditional again
$a = 0;
while ( $a < 10 ) {
    if ( $a == 5 ) {
        $a = $a + 1;
        redo;
    }
    print "Value of a = $a\n";
} continue {
    $a = $a + 1;
}
