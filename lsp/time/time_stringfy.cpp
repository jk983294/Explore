#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

/**
 * function()       single thread version
 * function_r()     multi thread version
 */

int main(void) {
    char buf[256] = "";

    time_t now;
    now = time(&now);

    ctime_r(&now, buf);
    printf("ctime_r: %s", buf);

    // convert time_t to struct tm
    struct tm tm;
    gmtime_r(&now, &tm);
    localtime_r(&now, &tm);

    // print struct tm
    asctime_r(&tm, buf);
    printf("asctime_r: %s", buf);

    // convert struct tm back to time_t
    time_t now1 = mktime(&tm);
    printf("difftime: %f\n", difftime(now1, now));
    return 0;
}
