int nCompletionStatus = 0;

double add(double x, double y) {
    double z = x + y;
    return z;
}

double add_and_multiply(double x, double y) {
    double z = add(x, y);
    z *= 3;
    return z;
}
