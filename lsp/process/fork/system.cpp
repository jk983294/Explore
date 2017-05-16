#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

// create a new process then wait for it
// better to use system which suit this case, don't use waitpid to mimic this behavior
int main(void) {
    int status;

    status = system("date");
    printf("%d\n", status);  // 0

    status = system("nosuchcommand");
    printf("%d\n", status);  // 32512

    status = system("who; exit 44");
    printf("%d\n", status);  // 11264
    return 0;
}
