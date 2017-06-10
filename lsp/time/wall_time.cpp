#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>  // timeval
#include <time.h>      // time_t timespec struct tm
#include <unistd.h>

/**
 * time_t           long                    second since epoch
 * timeval          tv_sec tv_usec          microseconds since epoch
 * timespec         tv_sec tv_nsec          nanoseconds since epoch
 * tm                                       human readable time sections, get from localtime_r gmtime_r
 */

int main(void) {
    time_t now;
    now = time(&now);
    printf("current time in seconds since the epoch: %ld\n", now);

    struct timeval tv;
    gettimeofday(&tv, NULL);
    printf("timeval: seconds=%ld, useconds=%ld\n", (long)tv.tv_sec, (long)tv.tv_usec);

    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    printf("timespec: seconds=%ld nsec=%ld\n", ts.tv_sec, ts.tv_nsec);
    return 0;
}
