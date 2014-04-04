import matplotlib.pyplot as plt
import numpy as np
import math
import geom_utils as gu

# Convert from decimal to sexagesimal
''' From http://idlastro.gsfc.nasa.gov/ftp/pro/astro/radec.pro '''
''' Need to put better testing in '''
def convertRA(ra):
    ra1 = math.trunc(ra/15.)
    ra2 = math.trunc((ra-ra1*15.)*4)
    ra3 = ((ra-ra1*15.-ra2/4.)*240.)

    return str(ra1) + ':' + str(ra2) + ':' + str(round(ra3,6))

def convertDEC(dec):
    dec1 = math.trunc(dec)
    dec2 = math.trunc(abs(dec-dec1)*60)
    dec3 = ((abs(dec-dec1)*60.)-dec2)*60.

    return str(dec1) + ':' + str(dec2) + ':' + str(round(dec3,6))

# Distance should be in parsec
def getDistMod(dist):
    return  5*math.log10(dist) - 5

'''
Add whatever correction, like a distance modulus, to a list of magnitudes
This function takes an array to correct
This isn't the right way to go about this...need to have the corrected mag
be in the catalog
'''
def correctMag(c, correction):
    return map(lambda c: c + correction , c)

'''
Cut out noise, good for DSIM input files...
Update this function to use filter() but be able to specify the element in the object
'''
def makeMagCut(mag, low, high):
    isGood = 0
    if mag <= high and mag >= low:
        isGood = 1
    return isGood

'''
This might need some tweaking with different colors.
'''
def makeColorCut(mag1, mag2, mag3, mag4, x0, x1, m, b, var):
    y_11 = gu.calcY(x1, m, b+var) # Top-right corner
    y_00 = gu.calcY(x0, m, b-var) # Lower-left corner, creates box that encompases GC locus

    px = mag1 - mag2
    py = mag3 - mag4
    if gu.inBox(x0, x1, y_00, y_11, px, py):
        return gu.inParallelogram(px, py,  m, b, var)

'''
Not sure how well this will work for other data sets.
'''
def detSizeCut(shape_col, bin_num):
    hist, bins = np.histogram(shape_col, bin_num)
    peak =  hist.argmax()

    return round(bins[peak+10], 4)

'''
This will will show a histogram of the input.
'''
def LookAtShapes(shape_col, bin_num):
    hist, bins = np.histogram(shape_col, bin_num)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

'''
Calculate the median of an array
'''
def calcMedian(data):
    data.sort()

    if len(data) % 2 == 1:
        return data[(len(data) + 1)/2 -1]
    else:
        lower = data[len(data)/2 -1]
        upper = data[len(data)/2]
        return (float(lower + upper))/2

'''
Calculate the median absolute deviation of an array
'''
def calcMAD(data):
    med = calcMedian(data)
    tmp = []
    for val in data:
        tmp.append(math.fabs(val - med))
    tmp.sort()
    return(calcMedian(tmp))

'''
Check for header on input files
'''
def noHead(line):
    if line[0] != "#":
        return True
    else:
        return False


#def testColorCut():
