#!/usr/bin/perl
use strict;
use warnings;

# valid characters
# @     list
# %     hash
# &     subroutine
# *     file handle
# \$    ref to scalar
# \@    ref to list
# \%    ref to hash

# example   $$,$ => two mandatory scalar, one optional scalar

sub accept_scalar ($) {
    my $param = shift;
    return ( $param, $param );
}

sub accept_array(@) {
    my @params = @_;
    print join '-', @params;
    print "\n";
}

accept_array( ( 1 .. 5 ) );

sub list_add(\@\@) {    # passed in two scalar, both are reference
    my @first  = @{$_[0]};
    my @second = @{$_[1]};
    my @result;

    while ( @first || @second ) {
        push @result, ( shift @first ) + ( shift @second );
    }
    return @result;
}

my @a = ( 1, 2, 3 );
my @b = ( 3, 4, 6, 1, 2 );
my @c = list_add( @a, @b );
print "@c\n";
