/*
// exec will replace current with specified binary
// execve is the actual system call, others just variation
// v vector, l list, e environment, p lookup program in PATH variable to execute
int execve(const char * filename,char * const argv[],char * const envp[]);
int execl(const char *pathname, char *arg0, char *arg1, ..., char *argn, NULL);
int execle(const char *pathname, char *arg0, char *arg1, ..., char *argn, NULL, char *envp[]);
int execlp(const char *pathname, char *arg0, char *arg1, ..., NULL);
int execlpe(const char *pathname, char *arg0, char *arg1, ..., NULL, char *envp[]);
int execv(const char *pathname, char *argv[]);
int execvp(const char *pathname, char *argv[]);
int execvpe(const char *pathname, char *argv[], char *envp[]);
*/
#include <unistd.h>

int main(int argc, char const* argv[]) {
    char* const args[] = {(char*)"ls", (char*)"-l", (char*)".", NULL};
    execv("/bin/ls", args);
    return 0;
}
