#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

/**
 * for small space allocation, glibc use malloc()
 * for large space allocation, glibc use anonymous mmap, it will auto init to 0 and page aligned
 */

int main(void) {
    void* p = mmap(NULL,                         // do not car where
                   512 * 1024,                   // 512K
                   PROT_READ | PROT_WRITE,       // rw
                   MAP_ANONYMOUS | MAP_PRIVATE,  // anonymous
                   -1,                           // fd ignored
                   0);                           // offset ignored

    // return back 512K
    munmap(p, 512 * 1024);
    return 0;
}
