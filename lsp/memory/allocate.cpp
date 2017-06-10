#include <stdlib.h>

/**
 * calloc will init memory to 0
 * malloc won't init memory to 0
 */

int main(void) {
    int* a = (int*)malloc(5 * sizeof(int));
    free(a);

    a = (int*)calloc(5, sizeof(int));
    a = (int*)realloc(a, 10 * sizeof(int));

    free(a);
    return 0;
}
