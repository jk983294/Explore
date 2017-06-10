#include <stdio.h>
#include <stdlib.h>

/**
 * valloc is the same with malloc but align with page size (getpagesize())
 * memalign is like posix_memalign but return the allocated address back
 *
 * prefer to choose posix_memalign because it is standard, the other two are not
 *
 * for class member, better to define data member by size descend
 */

int main(void) {
    char* buf;
    posix_memalign((void**)&buf, 256, 1024);  // allocate 1024 bytes align with 256-byte boundary
    free(buf);

    //!!! danger, may cause coredump depending on system, because char is 1 byte aligned while long is not
    char greeting[] = "hello world";
    char* c = greeting + 1;
    long badnews = *(long*)c;
    printf("%ld\n", badnews);
    return 0;
}
