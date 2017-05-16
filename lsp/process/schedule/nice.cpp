#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <unistd.h>

// (-20, 19], default 0, only root can have nice < 0

void set_absolute_nice(int value) {
    int current = nice(0);
    value = value - current;
    nice(value);
}

int main() {
    nice(5);               // increase by 5
    set_absolute_nice(6);  // set nice value to 6

    int value = getpriority(PRIO_PROCESS, 0);
    printf("nice value is %d\n", value);
    setpriority(PRIO_PROCESS, 0, 7);  // set nice value to 7
    value = getpriority(PRIO_PROCESS, 0);
    printf("nice value is %d\n", value);
    return 0;
}
