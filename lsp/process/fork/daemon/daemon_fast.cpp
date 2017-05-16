#include <stdio.h>
#include <unistd.h>

int daemon_work() {
    // add work code here
    return 0;
}

int main() {
    daemon(0, 0);
    while (1) {
        daemon_work();
        sleep(1);
    }
}
