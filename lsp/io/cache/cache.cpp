#include <stdio.h>

/**
 * _IONBF no buffer, stderr default
 * _IOLBF line buffer, terminal default
 * _IOFBF block buffer
 */

char buf[BUFSIZ];           // must use gloabal variable for buffer

const char* filename = "/tmp/tmp.txt";

int main(int argc, char const *argv[]) {
    // if buf is null, then glibc allocate buffer automatically
    setvbuf(stdout, buf, _IOFBF, BUFSIZ);
    printf("hello world!\n");
    return 0;
}
