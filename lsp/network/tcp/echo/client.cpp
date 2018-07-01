#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>  // define hostent

// usage: ./client localhost 8023

void error(const char *msg) {
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[]) {
    struct sockaddr_in serverAddr;
    char buffer[256];
    if (argc < 3) {
        fprintf(stderr, "usage %s hostname port\n", argv[0]);
        exit(0);
    }
    int portNo = atoi(argv[2]);
    if (!portNo) {
        servent *s = getservbyname(argv[2], "tcp");
        if (!s) {
            error("getservbyname() failed");
        }
        portNo = ntohs(static_cast<uint16_t>(s->s_port));
    }

    int sockFd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockFd < 0) error("ERROR opening socket");
    struct hostent *server = gethostbyname(argv[1]);  // DNS resolve to server info
    if (!server) {
        error("gethostbyname failed, no such host");
    }

    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    memcpy(&serverAddr.sin_addr.s_addr, server->h_addr_list[0], server->h_length);
    serverAddr.sin_port = htons(static_cast<uint16_t>(portNo));

    if (connect(sockFd, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0) error("ERROR connecting");

    printf("Please enter the message: ");
    memset(buffer, 0, 256);
    fgets(buffer, 255, stdin);
    long n = write(sockFd, buffer, strlen(buffer));
    if (n < 0) error("ERROR writing to socket");

    memset(buffer, 0, 256);
    n = read(sockFd, buffer, 255);
    if (n < 0) error("ERROR reading from socket");
    printf("%s\n", buffer);

    close(sockFd);
    return 0;
}
