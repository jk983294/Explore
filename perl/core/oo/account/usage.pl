#!/usr/bin/perl
use strict;
use BankAccount;
use Credit;

my $acc1 = BankAccount->new( "kun", 123, 10000 );
$acc1->deposit(5000);
$acc1->showBalance();
$acc1->show();

my $acc2 = new Credit( "jk", 123, 1000, 5000 );
$acc2->deposit(5000);
$acc2->showBalance();
$acc2->showLimit();
$acc2->show();
