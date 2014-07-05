#include <math.h>

long double angular_dist2(long double x1, long double y1,
                          long double x2, long double y2) {
    /* Simplified Law of Cosines
     * gamma = ((RA1 - RA2)cos(DEC1))^2 + (DEC1 - DEC2)^2 */
    long double a = ((x1-x2)*cos(y1))*((x1-x2)*cos(y1));
    long double b = (y1-y2)*(y1-y2);
    return a + b;
}

long double angular_dist(long double x1, long double y1, 
                         long double x2, long double y2) {
        return sqrt(angular_dist2(x1, y1, x2, y2));
}
