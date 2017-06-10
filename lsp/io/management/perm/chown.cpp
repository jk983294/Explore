#include <fcntl.h>
#include <grp.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    struct group *gr = getgrnam("kun");
    chown(argv[1], -1, gr->gr_gid);

    int fd = open(argv[1], O_RDONLY);
    fchown(fd, -1, gr->gr_gid);
    close(fd);
    return 0;
}
