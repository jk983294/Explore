#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// kill -USR2 6630

static void signal_handler(int signo) {
    if (signo == SIGUSR1)
        printf("Caught SIGUSR1!\n");
    else if (signo == SIGUSR2)
        printf("Caught SIGUSR2!\n");
    else {
        fprintf(stderr, "Unexpected signal\n");
        exit(EXIT_FAILURE);
    }
    exit(EXIT_SUCCESS);
}

int main(void) {
    if (signal(SIGUSR1, signal_handler) == SIG_ERR) {
        fprintf(stderr, "Cannot handle SIGUSR1\n");
        exit(EXIT_FAILURE);
    }

    if (signal(SIGUSR2, signal_handler) == SIG_ERR) {
        fprintf(stderr, "Cannot handle SIGUSR2\n");
        exit(EXIT_FAILURE);
    }

    if (signal(SIGPROF, SIG_DFL) == SIG_ERR) {  // default behaviour
        fprintf(stderr, "Cannot reset SIGPROF\n");
        exit(EXIT_FAILURE);
    }

    if (signal(SIGHUP, SIG_IGN) == SIG_ERR) {  // ignore this signal
        fprintf(stderr, "Cannot ignore SIGHUP\n");
        exit(EXIT_FAILURE);
    }

    for (;;) pause();

    return 0;
}
