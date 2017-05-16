#include <stdio.h>
#include <unistd.h>

int main(void) {
    pid_t sid;
    sid = getsid(0);
    printf("My session id=%d\n", sid);
    return 0;
}
