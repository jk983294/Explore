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
    struct hostent *hp;
    char buffer[256];

    if (argc != 3) {
        printf("Usage: server port\n");
        exit(1);
    }
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) error("socket");

    server.sin_family = AF_INET;
    hp = gethostbyname(argv[1]);
    if (hp == 0) error("Unknown host");

    bcopy((char *)hp->h_addr, (char *)&server.sin_addr, hp->h_length);
    server.sin_port = htons(atoi(argv[2]));
    unsigned int length = sizeof(struct sockaddr_in);

    printf("Please enter the message: ");
    bzero(buffer, 256);
    fgets(buffer, 255, stdin);

    int n = sendto(sock, buffer, strlen(buffer), 0, (const struct sockaddr *)&server, length);
    if (n < 0) error("Sendto");

    n = recvfrom(sock, buffer, 256, 0, (struct sockaddr *)&from, &length);
    if (n < 0) error("recvfrom");

    write(1, "Got an ack: ", 12);
    write(1, buffer, n);
    close(sock);
    return 0;
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}
