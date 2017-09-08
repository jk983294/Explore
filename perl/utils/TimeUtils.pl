#!/usr/bin/perl
use strict;
use warnings;
use DateTime;

package TimeUtils;

sub date {
    my @date = localtime();

    # array [5] = year since 1900, [4] = month from 0 .. 11, [3] = day
    $date[5] += 1900;
    $date[4] += 1;
    $date[4] = sprintf( "%02d", $date[4] );
    $date[3] = sprintf( "%02d", $date[3] );
    return "$date[5]$date[4]$date[3]";
}

sub getfancytime {
    my @time = localtime();
    return $time[2] . ":" . $time[1] . ":" . $time[0];
}

sub get_gmttime() {
    my @time = (localtime);
    my $date = DateTime->new(
        year      => $time[5] + 1900,
        month     => $time[4] + 1,
        day       => $time[3],
        hour      => $time[2],
        minute    => $time[1],
        second    => $time[0],
        time_zone => 'GMT'
    );
    return $date->strftime("%Y%m%d.%H%M%S");
}

1;    # file should end with true expression
