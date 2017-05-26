#!/usr/bin/perl
use strict;
use warnings;

sub creat_file {
    `echo "hello world" > /tmp/file1.txt`;
}

sub delete_file {
    unlink("/tmp/file2.txt");
}

sub rename_file {
    rename( "/tmp/file1.txt" => "/tmp/file2.txt" );
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
        push @description, 'binary'                   if ( -B $file );
        push @description, 'a socket'                 if ( -S $file );
        push @description, 'a text file'              if ( -T $file );
        push @description, 'a block special file'     if ( -b $file );
        push @description, 'a character special file' if ( -c $file );
        push @description, 'a directory'              if ( -d $file );
        push @description, 'executable'               if ( -x $file );
        push @description, 'modify time over 1 week'  if ( -M $file > 7 );
        push @description, ( ( $size = -s $file ) ) ? "$size bytes" : 'empty';
        print "$file is ", join( ', ', @description ), "\n";
    }

    if ( -r $file and -w _ ) {    # _ is virtual file handle, it is last file check stat object
        print "readable and writable\n";
    }

    if ( -T $file and -s _ < 512 ) {
        print "text file is less than 512 bytes\n";
    }

    if ( -r -w $file ) {          # stack check, from right to left check
        print "readable and writable\n";
    }
}

sub main {
    creat_file();
    file_information();
    rename_file();
    delete_file();
}

main();
