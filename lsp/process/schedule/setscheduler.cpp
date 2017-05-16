#include <sched.h>
#include <stdio.h>

void get_current_scheduler() {
    int policy = sched_getscheduler(0);
    switch (policy) {
        case SCHED_OTHER:
            printf("policy is normal\n");
            break;
        case SCHED_RR:
            printf("policy is round-robin\n");
            break;
        case SCHED_FIFO:
            printf("policy is first-in, first-out\n");
            break;
        case -1:
            perror("sched_getscheduler");
            break;
        default:
            fprintf(stderr, "Unknown policy!\n");
    }
}

int main(void) {
    get_current_scheduler();

    // set scheduler to RR
    struct sched_param sp = {.sched_priority = 1};
    struct timespec tp;
    sched_setscheduler(0, SCHED_RR, &sp);
    sched_getparam(0, &sp);
    printf("Our priority is %d\n", sp.sched_priority);
    sched_rr_get_interval(0, &tp);
    printf("Our time quantum is %.2lf milliseconds\n", (tp.tv_sec * 1000.0f) + (tp.tv_nsec / 1000000.0f));
    return 0;
}
