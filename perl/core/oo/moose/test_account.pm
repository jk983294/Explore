#!/usr/bin/perl
use strict;

package test_account;

use Test::Class;
use Test::More;
use base qw (Test::Class);

use BankAccount;
use Credit;

sub my_test : Test(2) {
    my $acc1 = BankAccount->new( name => "kun", accno => 123, balance => 10000 );
    is( $acc1->balance, 10000, "balance should be 10000" );
    $acc1->deposit(5000);
    is( $acc1->balance, 15000, "balance should be 15000" );
}

1;
