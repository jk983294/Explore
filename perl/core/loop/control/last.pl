
#!/usr/bin/perl
use strict;
use warnings;

# last statement is encountered inside a loop, the loop is immediately terminated
# last works like break in C/C++
$a = 10;
while ( $a < 20 ) {
    if ( $a == 15 ) {
        $a = $a + 1;    # terminate the loop.
        last;
    }
    print "value of a: $a\n";
    $a = $a + 1;
}

$a = 0;
OUTER: while ( $a < 4 ) {
    $b = 0;
    print "value of a: $a\n";
INNER: while ( $b < 4 ) {
        if ( $a == 2 ) {
            last OUTER;    # terminate outer loop
        }
        $b = $b + 1;
        print "Value of b : $b\n";
    }
    print "\n";
    $a = $a + 1;
}
