#!/usr/bin/perl
use strict;
use warnings;

sub sig_stop_handler {
    print "SIGTSTP catched\n";
}

sub sig_quit_handler {    # Ctrl + \
    print "SIGQUIT catched\n";
}

$SIG{'TSTP'} = \&sig_stop_handler;
$SIG{"QUIT"} = \&sig_quit_handler;

while (<STDIN>) {
    print;
}
