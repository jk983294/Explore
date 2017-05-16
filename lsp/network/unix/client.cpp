// usage: ./client localhost 8023
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

// usage: ./client /tmp/unix_socket_domain

void error(const char *);
int main(int argc, char *argv[]) {
    int sockfd;
    char buffer[82];

    struct sockaddr_un serv_addr;
    bzero((char *)&serv_addr, sizeof(serv_addr));
    serv_addr.sun_family = AF_UNIX;
    strcpy(serv_addr.sun_path, argv[1]);

    int servlen = strlen(serv_addr.sun_path) + sizeof(serv_addr.sun_family);
    if ((sockfd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) error("Creating socket");
    if (connect(sockfd, (struct sockaddr *)&serv_addr, servlen) < 0) error("Connecting");

    printf("Please enter your message: ");
    bzero(buffer, 82);
    fgets(buffer, 80, stdin);
    write(sockfd, buffer, strlen(buffer));

    read(sockfd, buffer, 80);
    printf("The return message was %s\n", buffer);
    close(sockfd);
    return 0;
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}
