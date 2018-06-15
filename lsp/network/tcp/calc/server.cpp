#include <arpa/inet.h>
#include <errno.h>
#include <memory.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <iostream>
#include "Data.h"

using namespace std;

Data data;

pthread_t new_thread(void (*work_func)(void*), void* args) {
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
    pthread_t thread_id;
    int r = pthread_create(&thread_id, &attr, (void* (*)(void*))work_func, args);
    pthread_attr_destroy(&attr);
    if (r != 0) {
        fprintf(stderr, "create thread error!\n");
        return 0;
    }
    return thread_id;
}

int sockSendUntil(int sockfd, char* buf, int toSend) {
    int rtn = 0;
    int sent = 0;
    char* pread = buf;
    while (sent < toSend) {
        rtn = send(sockfd, pread, toSend - sent, 0);
        if (rtn <= 0) {
            printf("send failed, sockfd:%d, errno:%d, already sent:%d, rtn:%d\n", sockfd, errno, sent, rtn);
            return rtn;
        }

        sent += rtn;
        pread += rtn;
    }  // while

    return toSend;
}

void sendData(void* args) {
    int sock = *(int*)args;
    while (true) {
        if (sockSendUntil(sock, (char*)&data, sizeof(data)) <= 0) {
            break;
        }
    }
}

#define BACKLOG 5  //定义侦听队列长度

int ss, sc;  // ss为服务器socket描述符，sc为某一客户端通信socket描述符

int main(int argc, char* argv[]) {
    struct sigaction sa;
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = SIG_IGN;
    sa.sa_flags = 0;
    sigaction(SIGPIPE, &sa, 0);

    data.i = 100 * 1000 * 1000L;
    data.d1 = 2.2;
    data.d2 = 2.22;
    data.name[0] = 0;

    int connectionCount = 0;

    if (argc < 2) {
        cout << "usage: ./server <bind port>" << endl;
        return -1;
    }
    short PORT = atoi(argv[1]);
    struct sockaddr_in server_addr;
    struct sockaddr_in client_addr;

    ss = socket(AF_INET, SOCK_STREAM, 0);
    if (ss < 0) {
        printf("server : server socket create error\n");
        return -1;
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    server_addr.sin_port = htons(PORT);

    int err;
    err = bind(ss, (struct sockaddr*)&server_addr, sizeof(sockaddr));
    if (err < 0) {
        printf("server : bind error\n");
        return -1;
    }

    err = listen(ss, BACKLOG);
    if (err < 0) {
        printf("server : listen error\n");
        return -1;
    }

    socklen_t addrlen = sizeof(client_addr);

    while (true) {
        cout << "accepting" << endl;
        sc = accept(ss, (struct sockaddr*)&client_addr, &addrlen);
        if (sc < 0) {
            cerr << "accept failed" << endl;
            return -1;
        }
        if (++connectionCount > 5) {
            cout << "too much connections:" << connectionCount << ", now quit" << endl;
        }
        cout << "accepted, total connections:" << connectionCount << endl;

        new_thread(sendData, &sc);

    }  // while
    return 0;
}
