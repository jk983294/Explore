#!/usr/bin/perl
use strict;
use warnings;

use LWP::Simple;

sub main {
    print "downloading...\n";

    # print get("www.baidu.com");

    my $code = getstore( "www.baidu.com", "index.html" );

    if ( $code == 200 ) {
        print "success\n";
    }
    else {
        print "failed\n";
    }

    print "finished\n";
}

main();
