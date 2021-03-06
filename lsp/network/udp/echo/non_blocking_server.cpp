#include <fcntl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <cerrno>

// usage: ./server 8023

void error(const char *msg);
void set_non_blocking(int fd);

int main(int argc, char *argv[]) {
    long n;
    struct sockaddr_in server;
    struct sockaddr_in client;
    char buf[1024 + 1];

    if (argc < 2) {
        fprintf(stderr, "ERROR, no port provided\n");
        exit(0);
    }

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) error("Opening socket");

    set_non_blocking(sock);

    int portNo = atoi(argv[1]);
    if (!portNo) {
        servent *s = getservbyname(argv[1], "tcp");
        if (!s) {
            error("getservbyname() failed");
        }
        portNo = ntohs(static_cast<uint16_t>(s->s_port));
    }

    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(static_cast<uint16_t>(portNo));

    if (bind(sock, (struct sockaddr *)&server, sizeof(server)) < 0) error("binding");  // probably already in use

    socklen_t clientLen = sizeof(struct sockaddr_in);
    while (1) {
        n = recvfrom(sock, buf, 1024, 0, (struct sockaddr *)&client, &clientLen);
        if (n < 0) {
            if (EAGAIN == errno || EINTR == errno ||
                errno == EWOULDBLOCK) {  // continue if interrupted or there is nothing to read
                continue;
            } else {
                error("recvfrom");
            }
        }
        buf[n] = '\0';
        printf("Received a datagram: %s", buf);
        n = sendto(sock, "Got your message\n", 17, 0, (struct sockaddr *)&client, clientLen);
        if (n < 0) error("sendto");
    }
}

void set_non_blocking(int fd) {
    int flag = fcntl(fd, F_GETFL, 0);
    if (flag < 0) {
        error("fcntl F_GETFL fail");
    }
    if (fcntl(fd, F_SETFL, flag | O_NONBLOCK) < 0) {
        error("fcntl F_SETFL fail");
    }
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}
