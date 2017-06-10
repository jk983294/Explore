#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, const char *argv[]) {
    link("/tmp/file.txt", "/tmp/file.hard.link");
    symlink("/tmp/file.txt", "/tmp/file.symbolic.link");

    unlink("/tmp/file.symbolic.link");
    unlink("/tmp/file.hard.link");  // won't get removed since link count not zero

    remove("/tmp/file.txt");
    return 0;
}
