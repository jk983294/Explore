#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

// usage: ./server /tmp/unix_socket_domain

void error(const char *);
int main(int argc, char *argv[]) {
    int sockfd;
    struct sockaddr_un cli_addr, serv_addr;
    char buf[80];

    if ((sockfd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) error("creating socket");

    bzero((char *)&serv_addr, sizeof(serv_addr));
    serv_addr.sun_family = AF_UNIX;
    strcpy(serv_addr.sun_path, argv[1]);
    int servlen = strlen(serv_addr.sun_path) + sizeof(serv_addr.sun_family);
    if (bind(sockfd, (struct sockaddr *)&serv_addr, servlen) < 0) error("binding socket");

    listen(sockfd, 5);
    socklen_t clilen = sizeof(cli_addr);
    int newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr, &clilen);
    if (newsockfd < 0) error("accepting");

    read(newsockfd, buf, 80);
    printf("receive msg: %s\n", buf);
    write(newsockfd, "I got your message\n", 19);

    close(newsockfd);
    close(sockfd);
    return 0;
}

void error(const char *msg) {
    perror(msg);
    exit(0);
}
