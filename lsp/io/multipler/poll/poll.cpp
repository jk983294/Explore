#include <fcntl.h>
#include <string.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/poll.h>
#include <unistd.h>
#include <stdio.h>

#define TIMEOUT 5

int main(int argc, char const *argv[]) {
    struct pollfd fds[2];
    fds[0].fd = STDIN_FILENO;
    fds[0].events = POLLIN;
    fds[1].fd = STDOUT_FILENO;
    fds[1].events = POLLOUT;
    int ret = poll (fds, 2, TIMEOUT * 1000);
    if (ret == -1) {
        perror("poll failed");
        return 1;
    } else if (!ret){
        printf("%d seconds elapsed.\n", TIMEOUT);
        return 0;
    }

    if(fds[0].events & POLLIN){
        printf("stdin is readable\n");
    }

    if(fds[1].events & POLLOUT){
        printf("stdout is writable\n");
    }
    return 0;
}
