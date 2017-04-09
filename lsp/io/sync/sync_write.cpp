#include <fcntl.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

const char* journal_filename = "/tmp/journal.log";

int main(int argc, char const *argv[]) {
    const char* entry = "hello world!\n";
    int fd = open (journal_filename, O_WRONLY | O_CREAT | O_APPEND, 0660);
    write (fd, entry, strlen (entry));

    // sync page to disk, otherwise OS would perform page cache optimization for performance
    // OS would like to collect more dirty write then flush once to actual disk
    fsync (fd);
    close (fd);
    return 0;
}
