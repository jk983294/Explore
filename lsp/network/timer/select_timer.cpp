#include <iostream>

using namespace std;

int main() {
    for (;;) {
        int n = fileno(stdin);
        fd_set fdSet;
        FD_ZERO(&fdSet);
        FD_SET(n, &fdSet);
        struct timeval tVal {
            1, 1000
        };
        if (select(n + 1, &fdSet, nullptr, nullptr, &tVal) == 1 && FD_ISSET(n, &fdSet)) {
            break;
        } else {
            cout << "timer" << endl;
        }
    }
    return 0;
}
