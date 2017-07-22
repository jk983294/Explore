#include <iostream>

#define FOR_EXPORT __attribute__((visibility("default")))
#define FOR_NON_EXPORT __attribute__((visibility("hidden")))

FOR_EXPORT void print_first();
