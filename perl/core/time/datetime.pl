#!/usr/bin/perl
use strict;
use warnings;
use DateTime;

my $dt = DateTime->from_epoch( epoch => time() );
printf "%4d%02d%02d\n", $dt->year, $dt->month, $dt->day;    # 20170522
print $dt->ymd, "\n";                                       # 2017-05-22
print $dt->ymd('/'), "\n";                                  # 2017/05/22
print $dt->ymd(''),  "\n";                                  # 20170522

# get duration
my $dt1 = DateTime->new( year => 1987, month => 12, day => 18 );
my $dt2 = DateTime->new( year => 2011, month => 5,  day => 1 );
my $duration = $dt2 - $dt1;
my @units    = $duration->in_units(qw(years months days));
printf "%d years, %d months, and %d days\n", @units;

# add duration to date
my $d = DateTime::Duration->new( days => 5 );
my $dt3 = $dt2 + $d;
print $dt3->ymd(''), "\n";                                  # 20110506
