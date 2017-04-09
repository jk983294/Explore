#include <stdio.h>
#include <unistd.h>

const char* filename = "/tmp/tmp.txt";

struct something
{
    char name[100];
    unsigned long booty;
    unsigned int beard_len;
} blackbeard = { "Edward Teach", 950, 48 };

int main(int argc, char const *argv[]) {
    FILE* out = fopen(filename, "w");

    if(!out){
        perror("fopen");
        return 1;
    }
    if(!fwrite(&blackbeard, sizeof(struct something), 1, out)){
        perror("fwrite");
        return 1;
    }

    /**
     * first fflush, flush data from user cache (glibc maintenacne) to kernel cache
     * then fsync flush data from kernel cache to disk
     */
    fflush(out);
    int fd = fileno(out);
    fsync (fd);

    if(fclose(out)){
        perror("fclose");
        return 1;
    }
    return 0;
}
