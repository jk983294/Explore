#!/usr/bin/perl
use strict;
use warnings;
use POSIX qw(strftime);

# sec,     # seconds of minutes from 0 to 61
# min,     # minutes of hour from 0 to 59
# hour,    # hours of day from 0 to 24
# mday,    # day of month from 1 to 31
# mon,     # month of year from 0 to 11
# year,    # year since 1900
# wday,    # days since sunday
# yday,    # days since January 1st
# isdst    # hours of daylight savings time
sub localtime_function {
    my @months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
    my @days   = qw(Sun Mon Tue Wed Thu Fri Sat Sun);

    my ( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst ) =
      localtime();
    print "$mday $months[$mon] $days[$wday]\n";

    my $datestring = localtime();
    print "Local date and time $datestring\n";
}

sub gmtime_function {
    my $datestring = gmtime();
    print "GMT date and time $datestring\n";
}

#  the numbers of seconds that have elapsed since a given date, in Unix is January 1, 1970.
sub epoch_time {
    my $epoc = time();
    print "Number of seconds since Jan 1, 1970 - $epoc\n";

    my $datestring = localtime($epoc);
    print "date and time from epoch time $datestring\n";
}

sub strftime_function {
    my $datestring = strftime "%a %b %e %H:%M:%S %Y", localtime;
    printf("date and time - $datestring\n");

    $datestring = strftime "%a %b %e %H:%M:%S %Y", gmtime;
    printf("date and time - $datestring\n");
}

sub time_format {
    my ( $sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst ) =
      localtime();
    printf("Time Format - HH:MM:SS\n");
    printf( "%02d:%02d:%02d", $hour, $min, $sec );
}

sub main {
    localtime_function();
    gmtime_function();
    epoch_time();
    strftime_function();
    time_format();
}

main();
