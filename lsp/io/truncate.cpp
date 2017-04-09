#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

const char* journal_filename = "/tmp/journal.log";

int main(int argc, char const *argv[]) {
    int ret = truncate (journal_filename, 5);
    if (ret < 0) {
        perror("truncate failed");
    }
    return 0;
}
