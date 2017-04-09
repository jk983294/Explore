#include <stdio.h>

/**
 * binary file can only work on the same machine
 * different machine has its own length, alignment policy
 */

const char* filename = "/tmp/tmp.txt";

struct something
{
    char name[100];
    unsigned long booty;
    unsigned int beard_len;
} p, blackbeard = { "Edward Teach", 950, 48 };

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
    if(fclose(out)){
        perror("fclose");
        return 1;
    }

    FILE* in = fopen(filename, "r");

    if(!in){
        perror("fopen");
        return 1;
    }
    if(!fread(&p, sizeof(struct something), 1, in)){
        perror("fread");
        return 1;
    }
    if(fclose(in)){
        perror("fclose");
        return 1;
    }

    printf("name=\"%s\" booty=%lu beard_len=%u\n", p.name, p.booty, p.beard_len);
    return 0;
}
