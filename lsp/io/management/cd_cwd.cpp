#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    size_t size = 256;
    char *ptr = new char[size];

    chdir("/usr/bin");
    getcwd(ptr, size);
    printf("cwd = %s\n", ptr);
    delete[] ptr;
    return 0;
}
