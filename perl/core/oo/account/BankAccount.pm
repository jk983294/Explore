#!/usr/bin/perl
package BankAccount;

use strict;
use warnings;

sub new {
    my ( $class, $name, $accno, $balance ) = @_;
    my $this = {'name' => $name, 'accno' => $accno, 'balance' => $balance,};
    bless $this, $class;    # hack namespace, let hash looks like a class
    return $this;
}

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

sub name {    # getter and setter, if contain argument, then setter, if no argument, then getter
    my ($this) = @_;
    @_ ? $this->{name} = shift : $this->{name};
}

1;
