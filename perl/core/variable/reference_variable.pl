#!/usr/bin/perl
use strict;
use warnings;

# reference is a scalar data type that holds the location of another value which could be scalar, arrays, or hashes
# C++ pointer

my $foo = 42;

sub hello {
    my ($value) = @_;
    print "hello $value\n";
}

sub creation {
    my $arrayref =
      [ 1, 2, [ 'a', 'b', 'c' ] ];    # a reference to an anonymous array
    my $hashref = {                   # a reference to an anonymous hash
        'Adam'  => 'Eve',
        'Clyde' => 'Bonnie',
    };
    my $coderef =
      sub { print "Boink!\n" };       # a reference to an anonymous subroutine

    my $bar  = 41;
    my @ages = ( 25, 30, 40 );
    my %data = ( 'John Paul', 45, 'Lisa', 30, 'Kumar', 40 );

    my $scalarref = \$bar;
    $arrayref = \@ages;
    $hashref  = \%data;
    $coderef  = \&hello;
    my $globref = \*foo;

    # dereferencing
    print "Value is : ", $$scalarref, "\n";    # 41
    print "Value is : ", @$arrayref,  "\n";    # 25 30 40
    print "Value is : ", %$hashref,   "\n";    # Lisa 30 John Paul 45 Kumar 40
    &$coderef($bar);                           # hello 41
    print "Value is : ", *$globref, "\n";      # *main::foo

    # ref type
    print "Reference type : ", ref($scalarref), "\n";    # SCALAR
    print "Reference type : ", ref($arrayref),  "\n";    # ARRAY
    print "Reference type : ", ref($hashref),   "\n";    # HASH
    print "Reference type : ", ref($coderef),   "\n";    # CODE
    print "Reference type : ", ref($globref),   "\n";    # GLOB
}

sub circular_references {
    my $foo = 100;
    $foo = \$foo;
    print "Value of foo is : ", $$foo, "\n";
}

sub main {
    creation();
    circular_references();
}

main();
