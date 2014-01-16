import math
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

'''
def makePlots():
    x = [1, 2, 3, 4]
    y = calcY(x, 0.48, -.23)
    y1 = calcY(x, 0.48, -.43)
    y2 = calcY(x, 0.48, -.03)
    plt.plot(x, y, linestyle='-', linewidth=3)
    plt.plot(x, y1, linestyle='-', linewidth=3)
    plt.plot(x, y2, linestyle='-', linewidth=3)
    plt.show()
'''

def calcY(x, m, b):
    y = m*x + b

    return y

def simpleComp(x0, x1, y0, y1, px, py):
    is_in = 0
    if px > x0 and px < x1 and py > y0 and py < y1:
        is_in = 1

    return is_in

def realComp(px, py,  m, b, var):
    is_in = 0
    y_top = calcY(px, m, b+var)
    y_bot = calcY(px, m, b-var)
    if py > y_bot and py < y_top:
        is_in = 1

    return is_in

def main():
    # Have the slope, y-intercept, and endpoints from M87 data
    b = -0.086
    m = 0.50
    x0 = 1.5
    x1 = 3.0
    var = 0.3

    # Find bounding points
    y_11 = calcY(x1, m, b+var)
    y_01 = calcY(x0, m, b+var)
    y_00 = calcY(x0, m, b-var)
    y_10 = calcY(x1, m, b-var)

    u_z = []
    g_z = []
    color1 = []
    color2 = [] # For selction testing

    output = open("colorCutCatalog.txt" , "w")
    with open('n4459_cfht_ugiz_auto.cat', 'r') as f:
        for object in (raw.strip().split() for raw in f):
            if object[0:1][0][0] != '#':
                px = float(object[3]) - float(object[9])
                py = float(object[5]) - float(object[9])
                color1.append(px)
                color2.append(py) # For selection testing
                # To an initial quick test of the posints
                in_bounds = simpleComp(x0, x1, y_00, y_11, px, py)

                # If the point is in the bounding box test to see if it's
                # in the parallelogram
                if in_bounds == 1:
                    yes = realComp(px, py, m, b, var)
                    #Write to new catalog
                    if yes:
                        u_z.append(float(object[3]) - float(object[9]))
                        g_z.append(float(object[5]) - float(object[9])) # For selection testing
                        output.write("%10s" % object[0] + "%15s" % object[1] +  "%15s" % object[2]
                            + "%15s" % object[3] + "%15s" % object[4] + "%15s" % object[5]
                            + "%15s" % object[6]+ "%15s" % object[7] + "%15s" % object[8]
                            + "%15s" % object[9] + "%15s" % object[10] + "%15s" % object[11]
                            + "%15s" % object[12] + "\n")

    # Check the selection
    x = [1.5, 2, 2.5, 3]
    y = [calcY(x[0], m, b), calcY(x[1], m, b),  calcY(x[2], m, b),  calcY(x[3], m, b)]
    yt = [calcY(x[0], m, b+var), calcY(x[1], m, b+var),  calcY(x[2], m, b+var),  calcY(x[3], m, b+var)]
    yb = [calcY(x[0], m, b-var), calcY(x[1], m, b-var),  calcY(x[2], m, b-var),  calcY(x[3], m, b-var)]

    plt.plot(color1, color2, linestyle='none', marker=',', alpha=0.1)
    plt.plot(u_z, g_z, linestyle='none', marker=',', alpha=0.7)
    plt.plot(x, y, linestyle='-', linewidth=1, color='r')
    plt.plot(x, yt, linestyle='-', linewidth=1, color='r')
    plt.plot(x, yb, linestyle='-', linewidth=1, color='r')
    plt.show()

if __name__ == "__main__":
    main()
