#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

// usage: ./server 8023

void error(const char *msg) {
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[]) {
    char buffer[256];
    struct sockaddr_in serverAddr, clientAddr;
    if (argc < 2) {
        fprintf(stderr, "ERROR, no port provided\n");
        exit(1);
    }
    int sockFd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockFd < 0) error("ERROR opening socket");

    int portNo = atoi(argv[1]);
    if (!portNo) {
        servent *s = getservbyname(argv[1], "tcp");
        if (!s) {
            error("getservbyname() failed");
        }
        portNo = ntohs(static_cast<uint16_t>(s->s_port));
    }

    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;  // INADDR_ANY gets the IP address of the machine
    serverAddr.sin_port =
        htons(static_cast<uint16_t>(portNo));  // convert a port number in host byte order to network byte order

    if (bind(sockFd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) {
        error("ERROR on binding");  // probably socket address already in use
    }

    listen(sockFd, 5);
    socklen_t clientLen = sizeof(clientAddr);

    int newSockFd = accept(sockFd,                          // binded socket
                           (struct sockaddr *)&clientAddr,  // this will get client info
                           &clientLen);
    if (newSockFd < 0) error("ERROR on accept");

    memset(buffer, 0, 256);
    long n = read(newSockFd, buffer, 255);
    if (n < 0) error("ERROR reading from socket");
    printf("Here is the message: %s\n", buffer);

    n = write(newSockFd, "I got your message", 18);
    if (n < 0) error("ERROR writing to socket");

    close(newSockFd);
    close(sockFd);
    return 0;
}
