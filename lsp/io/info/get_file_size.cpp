#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    struct stat sb;
    stat(argv[1], &sb);

    printf("%s is %ld bytes\n", argv[1], sb.st_size);
    return 0;
}
