#!/usr/bin/perl
use strict;
use warnings;

# system will create new process

system 'date';
system 'for i in *; do echo == $i ==; done';

# avoid '' shell cmd, use system call, however this will lose redirection and background task ability
my $target = '/home';
system 'ls', '-la', $target;

# exec won't create new process, current process will be replaced with new executable
exec 'date'
