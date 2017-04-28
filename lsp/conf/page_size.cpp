#include <stdio.h>
#include <unistd.h>

int main(int argc, char const *argv[]) {
    printf("page size: %d\n", getpagesize());
    printf("page size: %ld\n", sysconf(_SC_PAGESIZE));
    return 0;
}
