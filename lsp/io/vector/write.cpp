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
    const char* data[] = {
        "this is the first line.",
        "this is the second line.",
        "this is the third line."
    };

    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC);
    if(fd == -1){
        perror("open");
        return 1;
    }

    for (int i = 0; i < 3; i++) {
        iov[i].iov_base = (void*)(data[i]);
        iov[i].iov_len = strlen(data[i]);
        printf("string %d size %zu\n", i, iov[i].iov_len);
    }

    /**
     * vector write can combine several single normal write into one write opertion
     */
    ssize_t nr = writev(fd, iov, 3);
    if(nr == -1){
        perror("writev");
        return 1;
    }

    if (close(fd)) {
        perror("close");
    }
    return 0;
}
