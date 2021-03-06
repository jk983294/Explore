#!/usr/bin/perl
use strict;
use Socket;

# use port 8023 as default
my $port   = shift || 8023;
my $proto  = getprotobyname('tcp');
my $server = "localhost";

# create a socket, make it reusable
socket( SOCKET, PF_INET, SOCK_STREAM, $proto ) or die "Can't open socket $!\n";
setsockopt( SOCKET, SOL_SOCKET, SO_REUSEADDR, 1 ) or die "Can't set socket option to SO_REUSEADDR $!\n";

# bind to a port, then listen
bind( SOCKET, pack_sockaddr_in( $port, inet_aton($server) ) ) or die "Can't bind to port $port! \n";

listen( SOCKET, 5 ) or die "listen: $!";
print "SERVER started on port $port\n";

# accepting a connection
my $client_addr;
while ( $client_addr = accept( NEW_SOCKET, SOCKET ) ) {
    my $name = gethostbyaddr( $client_addr, AF_INET );
    print NEW_SOCKET "Smile from the server";
    print "Connection recieved from $name\n";
    close NEW_SOCKET;
}
