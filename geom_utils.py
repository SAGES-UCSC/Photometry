import math

import Quadtree_Utilities as utils

def calc_y(x, m, b):
    y = m*x + b
    return y

def in_box(x0, x1, y0, y1, px, py):
    is_in = 0
    if px > x0 and px < x1 and py > y0 and py < y1:
        is_in = 1
    return is_in

def in_parallelogram(px, py,  m, b, var):
    is_in = 0
    y_top = calcY(px, m, b+var)
    y_bot = calcY(px, m, b-var)
    if py > y_bot and py < y_top:
        is_in = 1
    return is_in

def radius_cut(ra, dec, gal_ra, gal_dec, distance):
    "All of these inputs need to be in degrees."
    if (math.sqrt((ra-gal_ra)**2) + math.sqrt((dec-gal_dec)**2)) <= distance:
        return 1
    else:
        return 0

def intersecting(b1xmin, b1xmax, b1ymin,
                 b1ymax, b2xmin, b2xmax,
                 b2ymin, b2ymax):
    "   "
    xmin = max(b1xmin, b2xmin)
    ymin = max(b1ymin, b2ymin)
    xmax = min(b1xmax, b2xmax)
    ymax = min(b1ymax, b2ymax)

    return (xmin < xmax and ymin < ymax)

def equnorm(x1, y1, x2, y2):
    return math.sqrt(equnorm2(x1, y1, x2, y2))

def equnorm2(x1, y1, x2, y2):
    a = ((x1-x2)*math.cos(y1))*((x1-x2)*math.cos(y1))
    b = (y1-y2)*(y1-y2)
    return a + b

def pixnorm(x1, y1, x2, y2):
    return math.sqrt(pixnorm2(x1, y1, x2, y2))

def pixnorm2(x1, y1, x2, y2):
    xd = x2 - x1
    yd = y2 -y1
    return xd * xd + yd * yd

