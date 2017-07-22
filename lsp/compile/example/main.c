#include "function.h"

extern int nCompletionStatus;

int main(int argc, char const *argv[]) {
    double x = 1.0;
    double y = 5.0;
    double z;
    z = add_and_multiply(x, y);
    nCompletionStatus = 1;
    return 0;
}
