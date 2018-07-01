#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <cstring>

int main() {
    int serverSockFd, clientSockFd;
    struct sockaddr_in serverAddress, clientAddress;
    fd_set readSet, testSet;
    char buffer[1024 + 1];
    const char *msg = "world";

    serverSockFd = socket(AF_INET, SOCK_STREAM, 0);
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddress.sin_port = htons(8023);

    socklen_t server_len = sizeof(serverAddress);
    bind(serverSockFd, (struct sockaddr *)&serverAddress, server_len);
    listen(serverSockFd, 5);  // max queue is 5

    FD_ZERO(&readSet);
    FD_SET(serverSockFd, &readSet);
    while (1) {
        int fd;
        long nRead;
        testSet = readSet;  // copy read set in case select modify it

        int result = select(FD_SETSIZE, &testSet, NULL, NULL, NULL);  // FD_SETSIZE system default fd
        if (result < 1) {
            perror("server select");
            exit(1);
        }

        for (fd = 0; fd < FD_SETSIZE; fd++) {
            if (FD_ISSET(fd, &testSet)) {
                if (fd == serverSockFd) {  // client request to connect
                    socklen_t clientLen = sizeof(clientAddress);
                    clientSockFd = accept(serverSockFd, (struct sockaddr *)&clientAddress, &clientLen);
                    FD_SET(clientSockFd, &readSet);
                    printf("new client coming on fd %d\n", clientSockFd);
                } else {  // client request data
                    nRead = read(fd, buffer, 1024);
                    if (nRead <= 0) {  // no data to read, client leave
                        close(fd);
                        FD_CLR(fd, &readSet);  // remove client fd
                        printf("client on fd %d leaving\n", fd);
                    } else {
                        printf("request from client %d : %s\n", fd, buffer);
                        write(fd, msg, strlen(msg));  // usually need to check write count to check if all sent
                    }
                }
            }
        }
    }
    return 0;
}
