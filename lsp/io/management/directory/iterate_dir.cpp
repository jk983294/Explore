#include <stdio.h>
#include <string.h>
#include <sys/dir.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

bool is_dir(const char *path) {
    struct stat st;
    lstat(path, &st);
    return 0 != S_ISDIR(st.st_mode);
}

void find_files(const char *path) {
    DIR *pdir;
    struct dirent *pdirent;
    char temp[1024];
    pdir = opendir(path);
    if (pdir) {
        while ((pdirent = readdir(pdir))) {
            // skip . and ..
            if (strcmp(pdirent->d_name, ".") == 0 || strcmp(pdirent->d_name, "..") == 0) continue;
            sprintf(temp, "%s/%s", path, pdirent->d_name);
            if (is_dir(temp)) {
                find_files(temp);
            } else {
                printf("%s\n", temp);
            }
        }
    } else {
        printf("opendir error:%s\n", path);
    }
    closedir(pdir);
}

int main(int argc, const char *argv[]) {
    find_files("/home/kun/github/hosts");
    return 0;
}
