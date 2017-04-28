#!/usr/bin/perl
use strict;
use warnings;

sub display_all_the_files_glob {
    my $dir = "/tmp/*";    # Display all the files in /tmp directory.
    $dir = "/tmp/*.c";     # Display all the C source files in /tmp directory.
    $dir = "/tmp/.*";      # Display all the hidden files.
    $dir =
      "/tmp/* /home/*"; # Display all the files from /tmp and /home directories.
    my @files = glob($dir);

    foreach (@files) {
        print $_ . "\n";
    }
}

sub display_all_the_files_opendir {
    opendir( DIR, '/tmp/' ) or die "Couldn't open directory, $!";
    while ( my $file = readdir DIR ) {
        print "$file\n";
    }
    closedir DIR;

    # print the list of C source files
    opendir( DIR, '/tmp/' ) or die "Couldn't open directory, $!";
    foreach ( sort grep( /^.*\.c$/, readdir(DIR) ) ) {
        print "$_\n";
    }
    closedir DIR;
}

sub create_new_directory {
    my $dir = "/tmp/perl";
    mkdir($dir) or die "Couldn't create $dir directory, $!";
    print "Directory created successfully\n";
}

# this directory should be empty before you try to remove it.
sub remove_new_directory {
    my $dir = "/tmp/perl";
    rmdir($dir) or die "Couldn't remove $dir directory, $!";
    print "Directory removed successfully\n";
}

sub change_a_directory {
    my $dir = "/home";
    chdir($dir) or die "Couldn't go inside $dir directory, $!";
    print "Your new location is $dir\n";
}

sub main {
    display_all_the_files_glob();
    display_all_the_files_opendir();
    create_new_directory();
    remove_new_directory();
    change_a_directory();
}

main();
