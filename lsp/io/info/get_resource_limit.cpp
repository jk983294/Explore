#include <stdio.h>
#include <sys/resource.h>
#include <sys/time.h>

// one process can get max resource supported by kernel
// soft limit < hard limit
int main(void) {
    struct rlimit rlim;
    getrlimit(RLIMIT_FSIZE, &rlim);
    printf("File size resource soft limit is %ld and hard limit is %ld\n", rlim.rlim_cur, rlim.rlim_max);
    return 0;
}
