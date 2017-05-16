#include <stdio.h>
#include <stdlib.h>

void cleanup(void) { printf("atexit() succeeded!\n"); }

int main(void) {
    if (atexit(cleanup) { // register function cleanup to run after process finish its life
        fprintf(stderr, "atexit(0 failed!\n");
        return 1;
    }
    return 0;
}
