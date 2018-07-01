#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

// usage: ./client localhost 8023

void error(const char *);
int main(int argc, char *argv[]) {
    struct sockaddr_in server, from;
    char buffer[256];

    if (argc != 3) {
        printf("Usage: server port\n");
        exit(1);
    }
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) error("socket");

    int portNo = atoi(argv[2]);
    if (!portNo) {
        servent *s = getservbyname(argv[2], "tcp");
        if (!s) {
            error("getservbyname() failed");
        }
        portNo = ntohs(static_cast<uint16_t>(s->s_port));
    }

    struct hostent *hp = gethostbyname(argv[1]);
    if (!hp) error("Unknown host");

    memset(&server, 0, sizeof(server));
    server.sin_family = AF_INET;
    memcpy(&server.sin_addr.s_addr, hp->h_addr_list[0], hp->h_length);
    server.sin_port = htons(static_cast<uint16_t>(portNo));

    printf("Please enter the message: ");
    memset(buffer, 0, 256);
    fgets(buffer, 255, stdin);

    long n = sendto(sock, buffer, strlen(buffer), 0, (const struct sockaddr *)&server, sizeof(server));
    if (n < 0) error("Sendto");

    socklen_t length = sizeof(struct sockaddr_in);
    n = recvfrom(sock, buffer, 256, 0, (struct sockaddr *)&from, &length);
    if (n < 0) error("recvfrom");

    buffer[n] = '\0';
    printf("Got an ack: %s", buffer);
    close(sock);
    return 0;
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}
