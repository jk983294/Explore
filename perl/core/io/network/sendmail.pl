#!/usr/bin/perl
use strict;
use warnings;

my $to      = 'jk983294@gmail.com';
my $from    = 'jk@yourdomain.com';
my $subject = 'Test Email';
my $message = 'This is test email sent by Perl Script';

open( MAIL, "|/usr/sbin/sendmail -t" );

# Email Header
print MAIL "To: $to\n";
print MAIL "From: $from\n";
print MAIL "Subject: $subject\n\n";

# Email Body
print MAIL $message;

close(MAIL);
print "Email Sent Successfully\n";
