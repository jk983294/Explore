#!/usr/bin/perl
use strict;
use warnings;
use DateTime;

package StringUtils;

sub trim {
    my $inStr = shift;
    $inStr =~ s/^\s+//;
    $inStr =~ s/\s+$//;
    return ($inStr);
}

sub reverseCase {
    my $inStr = shift;
    $inStr =~ tr/A-Za-z/a-zA-Z/;
    return ($inStr);
}

1;
