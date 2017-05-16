#include <fcntl.h>
#include <linux/fs.h>
#include <unistd.h>
#include <cstdlib>

#define NR_OPEN 1024

int main(void) {
    pid_t pid = fork();
    if (pid != 0) {
        exit(EXIT_SUCCESS);  // parent exit, leave child to be daemon
    }

    setsid();    // set daemon to new session and group
    chdir("/");  // go to root in case current dir be deleted

    // close all open files, NR_OPEN is overkill, but it works
    for (int i = 0; i < NR_OPEN; i++) close(i);

    // redirect fd's 0,1,2 to /dev/null
    open("/dev/null", O_RDWR);  // stdin
    dup(0);                     // stdout
    dup(0);                     // stderror

    // do its daemon thing

    return 0;
}
