#!/usr/bin/perl

@files = `ls *.cpp`;

foreach $file (@files) {
    @file_parts = split( '\.', $file );
    $file_no_extension = $file_parts[0];

    if ( !-e $file_no_extension ) {
        print $file;
        `g++ -c -std=c++11 -Wall -g $file`;
        `g++ $file_no_extension.o -o $file_no_extension -pthread -lboost_system`;
    }

}
