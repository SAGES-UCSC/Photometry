cimport c_norm

def norm(x1, y1, x2, y2):
    return c_norm.norm(x1, y1, x2, y2)
def norm2(x1, y1, x2, y2):
    return c_norm.norm2(x1, y1, x2, y2)
