#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>

// run as root, otherwise cannot lock such huge memory

const int alloc_size = 32 * 1024 * 1024;

int main() {
    char *memory = (char *)malloc(alloc_size);
    if (mlockall(MCL_CURRENT) == -1) {
        perror("mlockall");
        return (-1);
    }
    size_t i;
    size_t page_size = getpagesize();
    for (i = 0; i < alloc_size; i += page_size) {
        printf("i=%zd\n", i);
        memory[i] = 0;
    }

    if (munlockall() == -1) {
        perror("munlock");
        return (-1);
    }
    return 0;
}
