#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <cstring>

int main() {
    struct sockaddr_in address;
    int clientSockFd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = inet_addr("127.0.0.1");
    address.sin_port = htons(8023);
    int result = connect(clientSockFd, (struct sockaddr*)&address, sizeof(address));
    if (result < 0) {
        perror("connect error");
        exit(1);
    }

    const char* msg = "hello";
    write(clientSockFd, msg, strlen(msg));
    char buffer[1024 + 1];
    long n = read(clientSockFd, buffer, 1024);
    if (n > 0) {
        buffer[n] = '\0';
        printf("response from server = %s\n", buffer);
    }
    sleep(1);

    close(clientSockFd);
    return 0;
}
