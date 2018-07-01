#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

using namespace std;

int main(void) {
    const char *groupIp = "230.1.80.23";
    uint16_t groupPort = 8023;
    char buffer[1024 + 1];
    long n;
    int socketFd;
    struct sockaddr_in addr;  // group address
    struct ip_mreq mreq;
    socklen_t addrLen = sizeof(addr);

    socketFd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socketFd < 0) {
        perror("socket AF_INET");
        exit(1);
    }

    // allow multiple sockets to use the same port number
    u_int yes = 1;
    if (setsockopt(socketFd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0) {
        perror("setsockopt SO_REUSEADDR");
        exit(1);
    }

    // set up the destination group
    memset(&addr, 0, sizeof(struct sockaddr_in));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(groupPort);
    addr.sin_addr.s_addr = inet_addr(groupIp);

    // bind local address
    if (bind(socketFd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("binding the multicast");
        exit(1);
    }

    // request to join the multicast group
    mreq.imr_multiaddr.s_addr = inet_addr(groupIp);
    mreq.imr_interface.s_addr = htonl(INADDR_ANY);
    if (setsockopt(socketFd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
        perror("setsockopt IP_ADD_MEMBERSHIP");
        exit(1);
    }

    while (1) {
        n = recvfrom(socketFd, buffer, 1024, 0, (struct sockaddr *)&addr, &addrLen);
        if (n < 0) {
            printf("multicast recvfrom error!\n");
            exit(4);
        } else {
            buffer[n] = '\0';
            printf("recv msg: %s\n", buffer);
        }
    }
}
