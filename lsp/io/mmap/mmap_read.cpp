#include <fcntl.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char const *argv[]) {
    struct stat sb;
    off_t len;
    const char *p = "/tmp/mmap.file";
    int fd = open(p, O_RDONLY);

    if (fd == -1) {
        perror("open");
        return 1;
    }

    if (fstat(fd, &sb) == -1) {
        perror("fstat");
        return 1;
    }

    if (!S_ISREG(sb.st_mode)) {
        fprintf(stderr, "%s is not a file\n", p);
        return 1;
    }

    char *a = (char *)mmap(0, sb.st_size, PROT_READ, MAP_SHARED, fd, 0);
    if (a == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    if (close(fd) == -1) {
        perror("close");
        return 1;
    }

    for (len = 0; len < sb.st_size; len++) {
        putchar(a[len]);
    }

    if (munmap(a, sb.st_size) == -1) {
        perror("munmap");
        return 1;
    }
    return 0;
}
