#!/usr/bin/perl
use strict;
use warnings;
use utf8;

# Wide character in print at special_character.pl line 10.
# perl -CS special_character.pl

sub main {
    my $alef  = chr(0x05D0);
    my $alpha = chr( hex('03B1') );
    my $omega = chr(0x03C9);

    print $alef;
    print $alpha;
    print $omega;

    my $code_point = ord($alpha);
    print $code_point;
}

main();
