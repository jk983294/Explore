#!/usr/bin/perl
use strict;
use warnings;

my @a = ( "a\n", "b\n", "c\n" );
my @b = ( 'a',   'b',   'c' );

print @a;
print "@b\n";

print( 2 + 3 ) * 4;    # output is 5, and return value is 4

# format output
printf "%g %g %g\n", 5 / 2, 51 / 17, 51**8;    # 52.5 3 4.57679e+13
printf "%d\n",     17.85;                      # 17
printf "%6f\n",    17.85;                      # 17.850000
printf "%6.1f\n",  17.85;                      #   17.9
printf "%6.0f\n",  17.85;                      #     18
printf "%.2f%%\n", 5.63;                       # 5.63%

# right alignment
printf "---%6d---\n",  42;                     # ---    42---
printf "---%10s---\n", "hello";                # ---     hello---

#left alignment
printf "---%-10s---\n", "hello";               # ---hello     ---

# format array
printf "items are:\n" . ( "%10s\n" x @b ), @b;
