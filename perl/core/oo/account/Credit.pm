#!/usr/bin/perl
use warnings;

package Credit;

use base BankAccount;    # @ISA qw (BankAccount);

sub new {
    my ( $class, $name, $accno, $balance, $limit ) = @_;
    my $acct = $class->SUPER::new( $name, $accno, $balance );
    $acct->{limit} = $limit;
    bless $acct, $class;    # hack namespace twice
    return $acct;
}

sub showLimit {
    my ($this) = @_;
    print "Acc No: ", $this->{accno}, " - limit: ", $this->{limit}, "\n";
}

sub show {
    my ($this) = @_;
    $this->SUPER::show();
    print "Credit limit: ", $this->{limit}, "\n";
}

sub DESTORY {
    print "destory\n";
}

1;
