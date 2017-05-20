#!/usr/bin/perl
use strict;
use warnings;

my $file = "/tmp/file1.txt";

sub if_pattern {
    if ( open( DATA, $file ) ) {
    } else {
        die "Error: Couldn't open the file - $!";    # $! returns the actual error message
    }

    # Alternatively
    open( DATA, $file ) || die "Error: Couldn't open the file $!";
}

sub unless_pattern {
    unless ( chdir("/etc") ) {
        die "Error: Can't change directory - $!";
    }

    # Alternatively
    die "Error: Can't change directory!: $!" unless ( chdir("/etc") );
}

sub ternary_operator_pattern {
    my %data = ();
    print( exists( $data{'value'} ) ? 'There' : 'Missing', "\n" );
}

# raises a warning, a message is printed to STDERR, but no further action is taken
sub warn_pattern {
    chdir('/etc') or warn "Can't change directory";
}

# works just like warn, except that it also calls exit
sub die_pattern {
    chdir('/etc') or warn "Can't change directory";
}

sub main {
    if_pattern();
    unless_pattern();
    ternary_operator_pattern();
    warn_pattern();
    die_pattern();
}

main();
