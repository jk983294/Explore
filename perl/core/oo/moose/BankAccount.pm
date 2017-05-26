#!/usr/bin/perl
package BankAccount;

use strict;
use warnings;
use Moose;

has 'name'    => ( is => 'rw', isa => 'Str' );
has 'accno'   => ( is => 'rw', isa => 'Int', required => 1 );
has 'balance' => ( is => 'rw', isa => 'Int', default => 0 );

sub deposit {
    my ( $this, $money ) = @_;
    $this->{balance} += $money;
}

sub showBalance {
    my ($this) = @_;
    print "Acc No: ", $this->{accno}, " - balance: ", $this->{balance}, "\n";
}

sub show {
    my ($this) = @_;
    print "name: ", $this->{name}, " Acc No: ", $this->{accno}, " - balance: ", $this->{balance}, "\n";
}


1;
