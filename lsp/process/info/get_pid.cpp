#include <stdint.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    printf("My pid is %jd\n", (intmax_t)getpid());
    printf("Parent pid is %jd\n", (intmax_t)getppid());
    return 0;
}
