#!/usr/bin/perl
use strict;
use warnings;

sub delete_file {
    unlink("/tmp/file1.txt");
}

sub rename_file {
    rename( "/tmp/file1.txt", "/tmp/file2.txt" );
}

# -A        Script start time minus file last access time, in days.
# -B        Is it a binary file?
# -C        Script start time minus file last inode change time, in days.
# -M        Script start time minus file modification time, in days.
# -O        Is the file owned by the real user ID?
# -R        Is the file readable by the real user ID or real group?
# -S        Is the file a socket?
# -T        Is it a text file?
# -W        Is the file writable by the real user ID or real group?
# -X        Is the file executable by the real user ID or real group?
# -b        Is it a block special file?
# -c        Is it a character special file?
# -d        Is the file a directory?
# -e        Does the file exist?
# -f        Is it a plain file?
# -g        Does the file have the setgid bit set?
# -k        Does the file have the sticky bit set?
# -l        Is the file a symbolic link?
# -o        Is the file owned by the effective user ID?
# -p        Is the file a named pipe?
# -r        Is the file readable by the effective user or group ID?
# -s        Returns the size of the file, zero size = empty file.
# -t        Is the filehandle opened by a TTY (terminal)?
# -u        Does the file have the setuid bit set?
# -w        Is the file writable by the effective user or group ID?
# -x        Is the file executable by the effective user or group ID?
# -z        Is the file size zero?
sub file_information {
    my $file = "/tmp/file1.txt";
    my ( @description, $size );
    if ( -e $file ) {
        push @description, 'binary'                   if ( -B _ );
        push @description, 'a socket'                 if ( -S _ );
        push @description, 'a text file'              if ( -T _ );
        push @description, 'a block special file'     if ( -b _ );
        push @description, 'a character special file' if ( -c _ );
        push @description, 'a directory'              if ( -d _ );
        push @description, 'executable'               if ( -x _ );
        push @description, ( ( $size = -s _ ) ) ? "$size bytes" : 'empty';
        print "$file is ", join( ', ', @description ), "\n";
    }
}

sub main {
    file_information();
    rename_file();
    delete_file();
}

main();
