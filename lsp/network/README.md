# Linux Network Programming

## legacy api
getservbyname(service, protocol);       // check /etc/services  => get back servent => sockaddr_in.sin_port
gethostbyname(host);                    // check /etc/hosts     => get back hostent => sockaddr_in.sin_addr

## new api
getaddrinfo()

## easy client check using telnet
telnet localhost 8023
