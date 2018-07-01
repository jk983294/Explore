#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <iostream>

using namespace std;

int main(void) {
    const char* groupIp = "230.1.80.23";
    uint16_t groupPort = 8023;
    char buffer[1024 + 1];
    long n;
    int socketFd;
    struct sockaddr_in groupAddr;  // group address

    socketFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socketFd < 0) {
        perror("socket AF_INET");
        exit(1);
    }

    // allow multiple sockets to use the same port number
    u_int yes;
    if (setsockopt(socketFd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0) {
        perror("setsockopt SO_REUSEADDR");
        exit(1);
    }

    // set up the destination group
    memset(&groupAddr, 0, sizeof(struct sockaddr_in));
    groupAddr.sin_family = AF_INET;
    groupAddr.sin_port = htons(groupPort);
    groupAddr.sin_addr.s_addr = inet_addr(groupIp);

    int count = 0;
    while (1) {
        ++count;
        sprintf(buffer, "current count is %d", count);

        n = sendto(socketFd, buffer, strlen(buffer), 0, (struct sockaddr*)&groupAddr, sizeof(struct sockaddr_in));
        if (n < 0) {
            printf("sendto error!\n");
            exit(3);
        }
        sleep(1);
    }
}
