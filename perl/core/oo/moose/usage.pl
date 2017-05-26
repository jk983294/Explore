#!/usr/bin/perl
use strict;
use BankAccount;
use Credit;

my $acc1 = BankAccount->new( name => "kun", accno => 123, balance => 10000 );
$acc1->deposit(5000);
$acc1->showBalance();
$acc1->show();

my $acc2 = new Credit( name => "jk", accno => 123, balance => 1000, limit => 5000 );
$acc2->deposit(5000);
$acc2->showBalance();
$acc2->showLimit();
$acc2->show();
