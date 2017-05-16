#include <sched.h>
#include <stdio.h>

int main(void) {
    int min, max;

    min = sched_get_priority_min(SCHED_RR);
    max = sched_get_priority_max(SCHED_RR);
    printf("SCHED_RR priority range is %d - %d\n", min, max);
    return 0;
}
