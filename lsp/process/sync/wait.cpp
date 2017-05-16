#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

// if status is not NULL, then it carry some extra info of child process
int main(void) {
    if (!fork()) {
        // child process action
        return 1;  // Normal termination with exit status=1
        // abort();   // Killed by signal=6 (dumped core)
    }

    int status;
    pid_t pid = wait(&status);
    printf("pid=%d\n", pid);

    if (WIFEXITED(status))
        printf("Normal termination with exit status=%d\n", WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
        printf("Killed by signal=%d%s\n", WTERMSIG(status), WCOREDUMP(status) ? " (dumped core)" : "");
    else if (WIFSTOPPED(status))
        printf("Stopped by signal=%d\n", WSTOPSIG(status));
    else if (WIFCONTINUED(status))
        printf("Continued\n");
    return 0;
}
