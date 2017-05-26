#!/usr/bin/perl
use warnings;

package Credit;
use Moose;

extends 'BankAccount';

has 'limit' => ( is => 'rw', isa => 'Int', default => 0 );

sub showLimit {
    my ($this) = @_;
    print "Acc No: ", $this->{accno}, " - limit: ", $this->{limit}, "\n";
}

sub show {
    my ($this) = @_;
    $this->SUPER::show();
    print "Credit limit: ", $this->{limit}, "\n";
}

1;
