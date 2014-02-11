def calcY(x, m, b):
    y = m*x + b
    return y

def inBox(x0, x1, y0, y1, px, py):
    is_in = 0
    if px > x0 and px < x1 and py > y0 and py < y1:
        is_in = 1
    return is_in

def inParallelogram(px, py,  m, b, var):
    is_in = 0
    y_top = calcY(px, m, b+var)
    y_bot = calcY(px, m, b-var)
    if py > y_bot and py < y_top:
        is_in = 1
    return is_in

'''
All of these inputs need to be in degrees.
'''
def makeRadiusCut(ra, dec, gal_ra, gal_dec, distance):
    if (math.sqrt((ra-gal_ra)**2) + math.sqrt((dec-gal_dec)**2)) <= distance:
        return 1
    else:
        return 0

'''
Specifically for use with the quadtree
Takes two Box objects as arguments
'''
def intersecting(b1, b2):
    if (b1.xmin >= b2.xmin and b1.xmin < b2.xmax) or \
        (b1.xmax >= b2.xmin and b1.xmax < b2.xmax) or \
        (b1.xmin <= b2.ymin and b1.xmax >= b2.xmax) or \
        (b1.xmin >= b2.xmin and b1.xmax <= b2.xmax):

        if (b1.ymin >= b2.ymin and b1.ymin < b2.ymax) or \
            (b1.ymax >= b2.ymin and b1.ymax < b2.ymax) or \
            (b1.ymin <= b2.ymin and b1.ymax >= b2.ymax) or \
            (b1.ymin >= b2.ymin and b1.ymax <= b2.ymax):

            return 1

        return 0

def norm(x1, y1, x2, y2):
    return sqrt(norm2(x1, y1, x2, y2))

'''
Do this to optimize for when you only care about relative distances
'''
def norm2(x1, y1, x2, y2):
    xd = x2 - x1
    yd = y2 -y1
    return xd * x2 + yd * yd

def dblmax(a, b):
    if a > b:
        return a
    else:
        return b

def dblmin(a, b):
    if a < b:
        return a
    else:
        return b
'''
'''
def clip_box(bxmin, bxmax, bymin, bymax, boundsxmin, boundsxmax, boundsymin, boundsymax):
    bxmin = dblmax(bxmin, boundsxmin)
    bymin = dblmax(bymin, boundsymin)
    bxmax = dblmin(bxmax, boundsxmax)
    bymax = dblmin(bymax, boundsymax)
