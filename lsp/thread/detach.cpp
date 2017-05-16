#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void *threadFunc(void *pArg) {
    printf("thread sleep\n");
    sleep(10);
    printf("this should not show since main finish before\n");
    pthread_exit(NULL);
}

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, threadFunc, NULL);
    pthread_detach(tid);
    printf("main finish before thread\n");
    return 0;
}
