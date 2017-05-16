#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();
    if (!pid) {
        printf("child!\n");
        exit(0);
    } else {
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) printf("child process exit success with status %d\n", WEXITSTATUS(status));
    }
    return 0;
}
