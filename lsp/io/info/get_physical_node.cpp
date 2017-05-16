#include <fcntl.h>
#include <linux/fs.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int get_physical_block(int fd, int logic_block) {
    int physical_block = -1;
    ioctl(fd, FIBMAP, &physical_block);
    return physical_block;
}

int get_logic_block_count(int fd) {
    struct stat buf;
    fstat(fd, &buf);
    return buf.st_blocks;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);

    int block_count = get_logic_block_count(fd);
    for (int i = 0; i < block_count; i++) {
        int physical_block = get_physical_block(fd, i);
        printf("(%u, %u) ", i, physical_block);
    }
    close(fd);
    return 0;
}
