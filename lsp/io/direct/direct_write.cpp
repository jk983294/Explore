#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

const char* journal_filename = "/tmp/journal.log";

int main(int argc, char const *argv[]) {
    const char* entry = "hello world!\n";
    // O_DIRECT means OS give up page cache optimization
    int fd = open (journal_filename, O_WRONLY | O_CREAT | O_APPEND | O_DIRECT, 0660);
    write (fd, entry, strlen (entry));
    close (fd);
    return 0;
}
