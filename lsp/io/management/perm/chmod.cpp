#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    chmod(argv[1], S_IRUSR | S_IWUSR);

    int fd = open(argv[1], O_RDONLY);
    fchmod(fd, S_IRUSR | S_IWUSR);
    close(fd);
    return 0;
}
