#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/uio.h>

const char* filename = "/tmp/tmp.txt";

int main(int argc, char const *argv[]) {
    struct iovec iov[3];
    char foo[23], bar[24], baz[23];

    int fd = open(filename, O_RDONLY);
    if(fd == -1){
        perror("open");
        return 1;
    }

    iov[0].iov_base = foo;
    iov[0].iov_len = sizeof(foo);
    iov[1].iov_base = bar;
    iov[1].iov_len = sizeof(bar);
    iov[2].iov_base = baz;
    iov[2].iov_len = sizeof(baz);

    /**
     * vector read can combine several single normal read into one read opertion
     */
    ssize_t nr = readv(fd, iov, 3);
    if(nr == -1){
        perror("readv");
        return 1;
    }

    if (close(fd)) {
        perror("close");
    }

    for (int i = 0; i < 3; i++) {
        printf("%d: %s\n", i, (char*)iov[i].iov_base);
    }
    return 0;
}
