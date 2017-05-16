#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

// fork(), child return 0, parent return child's pid
int main(int argc, char** argv) {
    if (!fork()) {
        printf("parent * ppid = %d, pid = %d *\n", getppid(), getpid());
    } else {
        sleep(2);
        printf("child # ppid = %d, pid = %d #\n", getppid(), getpid());
        printf("going to exec different binary in this process\n");
        char* const args[] = {(char*)"ls", (char*)"-l", (char*)".", NULL};
        execv("/bin/ls", args);
    }
    return 0;
}
