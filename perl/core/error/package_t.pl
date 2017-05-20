package T;

require Exporter;
@ISA    = qw/Exporter/;
@EXPORT = qw/function/;
use Carp;

sub function_warn {

    # warn: prints the message to STDERR, then exiting the script and printing the script name
    warn "Error in module!";
}

sub function_carp {

    # carp: warn and prints the message to STDERR without actually exiting the script and printing the script name
    carp "Error in module!";
}
1;
