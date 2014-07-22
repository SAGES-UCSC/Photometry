cdef extern from "norm.h":
    long double norm(long double x1, long double y1, long double x2, long double y2)
    long double norm22(long double x1, long double y1, long double x2, long double y2)
