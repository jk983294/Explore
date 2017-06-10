#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void dup_string(const char* data) {
    char* dup = (char*)alloca(strlen(data) + 1);
    strcpy(dup, data);
    // manipulate dup
    printf("%s\n", dup);
    return;  // dup is automatically freed
}
int main(void) {
    dup_string("hello world");
    dup_string("const char *data");
    return 0;
}
