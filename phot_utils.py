import matplotlib.pyplot as plt
import numpy as np
import math
import geom_utils as gu


'''
All of these inputs need to be in degrees.
'''
def makeRadiusCut(ra, dec, gal_ra, gal_dec, distance):
    if (math.sqrt((ra-gal_ra)**2) + math.sqrt((dec-gal_dec)**2)) <= distance:
        return 1
    else:
        return 0

'''
This might need some tweaking with different colors.
'''
def makeColorCut(mag1, mag2, mag3, mag4, x0, x1, m, b, var):
    y_11 = gu.calcY(x1, m, b+var) # Top-right corner
    y_00 = gu.calcY(x0, m, b-var) # Lower-left corner, creates box that encompases GC locus

    px = mag1 - mag3
    py = mag2 - mag4
    if gu.inBox(x0, x1, y_00, y_11, px, py):
        return gu.inParallelogram(px, py,  m, b, var)

'''
Not sure how well this will work for other data sets.
'''
def detHistPeak(shape_col, bin_num):
    hist, bins = np.histogram(shape_col, bin_num)
    peak =  hist.argmax()

    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
    return round(bins[peak+10], 4)

#def testRadiusCut():

#def testColorCut():
