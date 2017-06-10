#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>    // nanosleep
#include <unistd.h>  // sleep usleep

/**
 * sleep                second
 * usleep               microsecond
 * nanosleep            nanosecond
 */

int main(void) {
    sleep(1);     // one second
    usleep(500);  // half second

    struct timespec req = {.tv_sec = 0, .tv_nsec = 500 * 1000 * 1000};
    nanosleep(&req, NULL);  // half second

    // sleep to absoulte time based on current time, because several function call will consume some time
    clock_gettime(CLOCK_MONOTONIC, &req);
    req.tv_sec += 1;
    clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &req, NULL);  // one second
    return 0;
}
