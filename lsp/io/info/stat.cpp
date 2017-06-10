#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "usage: %s <file>\n", argv[0]);
        return 1;
    }

    struct stat sb;
    stat(argv[1], &sb);

    printf("%s:\n", argv[1]);
    printf("in device %ld, is on physical device: %u\n", sb.st_dev, gnu_dev_major(sb.st_dev));
    printf("inode: %ld\n", sb.st_ino);
    printf("permission: %o\n", sb.st_mode);
    printf("hard link: %ld\n", sb.st_nlink);
    printf("user id: %u\n", sb.st_uid);
    printf("group id: %u\n", sb.st_gid);
    printf("device: %ld\n", sb.st_rdev);
    printf("%ld bytes\n", sb.st_size);
    printf("best buffer size: %ld bytes\n", sb.st_blksize);
    printf("number of block allocated: %ld\n", sb.st_blocks);
    printf("access time: %s", ctime(&sb.st_atime));
    printf("content modified time: %s", ctime(&sb.st_mtime));
    printf("meta data modified time: %s", ctime(&sb.st_ctime));
    return 0;
}
