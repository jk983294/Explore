#include <dlfcn.h>
#include <iostream>

using namespace std;

typedef void (*TFunc)();

int main(int argc, char const *argv[]) {
    void *pHandle;
    pHandle = dlopen("libdynamiclib.so", RTLD_LAZY);
    if (NULL == pHandle) {
        cerr << dlerror() << endl;
        return -1;
    }

    /**
     * here we can only find print_second symbol because it is protected by extern C idiom
     * we cannot find print_first symbol since it is mangled by c++ compiler
     */
    TFunc f = (TFunc)dlsym(pHandle, "print_second");
    if (NULL == f) {
        cerr << dlerror() << endl;
        dlclose(pHandle);
        pHandle = NULL;
        return -1;
    }

    f();
    dlclose(pHandle);
    pHandle = NULL;
    return 0;
}
