#include <sched.h>
#include <stdio.h>

#define MAX_CPU 8

void display_affinity(cpu_set_t &set) {
    for (int i = 0; i < MAX_CPU; i++) {
        int cpu = CPU_ISSET(i, &set);
        printf("cpu=%i is %s\n", i, cpu ? "set" : "unset");
    }
}

void get_current_affinity() {
    cpu_set_t set;
    CPU_ZERO(&set);
    sched_getaffinity(0, sizeof(cpu_set_t), &set);
    display_affinity(set);
}

void set_affinity() {
    cpu_set_t set;
    CPU_ZERO(&set);    // clear all CPU
    CPU_SET(0, &set);  // allow CPU #0
    CPU_CLR(1, &set);  // disallow CPU #1
    sched_setaffinity(0, sizeof(cpu_set_t), &set);
    display_affinity(set);
}

int main(void) {
    get_current_affinity();
    set_affinity();
    return 0;
}
