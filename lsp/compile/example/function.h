#pragma once

#define FIRST_OPTION
#ifdef FIRST_OPTION
#define MULTIPLER (3.0)
#else
#define MULTIPLER (2.0)
#endif

double add_and_multiply(double x, double y);
