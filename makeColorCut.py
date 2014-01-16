'''
AUTHOR
    Alexa Villaume, UCSC

PURPOSE
    Make a color cut to select potential Globular Cluster candidates

INPUT PARAMETERS
    As of now this program is not set up to take command line arguments.
    You have to hard code the following:
    1.) The path to both the input and output files (output)
    2.) The slope and y-intercept of a known GC locus to make the cut (b, m, x0, x1)
    3.) The column number of the relevant magnitudes (px, py)
    4.) How strict the cut is going to be (var)

FILES CREATED
    The ouput catalog
    A plot is also generated to check the results of the catalog

NOTES
    The selection is based on having a line of where the the GC candidates should be.
    We used M87 data, which has a spectroscopically confirmed GC population to make a
    guess of where the GC population should be for other galaxies.

    Future versions of this program are going to be generalized so that it can be included
    easily in larger programs.
'''


import math
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

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
    var = 0.3   # This controls how strict the cut is

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

                # To an initial quick test of the points
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

    plt.plot(color1, color2, linestyle='none', marker=',', alpha=0.1) # Full list
    plt.plot(u_z, g_z, linestyle='none', marker=',', alpha=0.7) # Colors that made the cut
    plt.plot(x, y, linestyle='-', linewidth=1, color='r')
    plt.plot(x, yt, linestyle='-', linewidth=1, color='r')
    plt.plot(x, yb, linestyle='-', linewidth=1, color='r')  # The boudding region
    plt.show()

if __name__ == "__main__":
    main()
