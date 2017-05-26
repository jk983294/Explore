#!/usr/bin/perl
use strict;
use warnings;
use File::Spec;
use File::Basename qw/ basename /;    # only import basename function

# use File::Basename ();              # not import in case pollute namespace

my $name     = "/usr/local/bin/perl";
my $base     = basename($name);
my $dirname  = File::Basename::dirname($name);
my $new_name = File::Spec->catfile( $dirname, $base );    # in case different os has different file delimiter
print "$base $dirname $new_name $name\n";
