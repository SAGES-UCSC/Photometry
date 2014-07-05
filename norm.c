#include <math.h>

long double norm2(long double x1, long double y1, long double x2, long double y2) {
    long double xd = x2 - x1;
    long double yd = y2 - y1;
    return xd * xd + yd * yd;
}

long double norm(long double x1, long double y1, long double x2, long double y2) {
    return sqrt(norm2(x1, y1, x2, y2));
}
