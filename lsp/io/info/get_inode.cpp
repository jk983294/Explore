#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int get_inode(int fd) {
    struct stat buf;
    fstat(fd, &buf);
    return buf.st_ino;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    int inode = get_inode(fd);
    printf("%d\n", inode);
    close(fd);
    return 0;
}
