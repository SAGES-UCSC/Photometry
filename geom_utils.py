import math

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
'''
def intersecting(b1xmin, b1xmax, b1ymin, b1ymax, b2xmin, b2xmax, b2ymin, b2ymax):
    if (b1xmin >= b2xmin and b1xmin < b2xmax) or \
        (b1xmax >= b2xmin and b1xmax < b2xmax) or \
        (b1xmin <= b2ymin and b1xmax >= b2xmax) or \
        (b1xmin >= b2xmin and b1xmax <= b2xmax):

        if (b1ymin >= b2ymin and b1ymin < b2ymax) or \
            (b1ymax >= b2ymin and b1ymax < b2ymax) or \
            (b1ymin <= b2ymin and b1ymax >= b2ymax) or \
            (b1ymin >= b2ymin and b1ymax <= b2ymax):

            return 1

        return 0

def norm(x1, y1, x2, y2):
    return math.sqrt(norm2(x1, y1, x2, y2))

'''
Do this to optimize for when you only care about relative distances
'''
def norm2(x1, y1, x2, y2):
    xd = x2 - x1
    yd = y2 -y1
    return xd * xd + yd * yd

'''
'''
def clip_box(bxmin, bymin, bxmax, bymax, boundsxmin, boundsymin, boundsxmax, boundsymax):
    return {'xmin' : min(bxmin, boundsxmin), 'ymin' : min(bymin, boundsymin),
            'xmax' : max(bxmax, boundsxmax), 'ymax' : max(bymax, boundsymax)}
