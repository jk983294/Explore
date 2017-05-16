#include <pthread.h>
#include <stdio.h>

#define NUM_THREADS 4

void *threadFunc(void *pArg) {
    pthread_t tid = pthread_self();
    int myNum = *((int *)pArg);
    printf("Thread %ld number %d\n", tid, myNum);
    pthread_exit(NULL);  // the same as return NULL;
}

int main() {
    pthread_t tid[NUM_THREADS];
    int *data = new int[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        data[i] = i;
        pthread_create(&tid[i], NULL, threadFunc, &data[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(tid[i], NULL);
    }
    return 0;
}
