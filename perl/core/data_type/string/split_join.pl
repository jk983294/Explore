#!/usr/bin/perl
use strict;
use warnings;

sub main {
    my $var_string = "Rain-Drops-On-Roses-And-Whiskers-On-Kittens";
    my $var_names  = "Larry,David,Roger,Ken,Michael,Tom";

    # transform above strings into arrays.
    my @string = split( '-', $var_string );
    my @names  = split( ',', $var_names );

    print "$string[3]\n";    # Roses
    print "$names[4]\n";     # Michael

    my $string1 = join( '-', @string );
    my $string2 = join( ',', @names );

    print "$string1\n";
    print "$string2\n";
}

main();
