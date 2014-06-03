import matplotlib.pyplot as plt
import os
import numpy as np
import math
import Sources as sources
from astropy.io import fits
import geom_utils as gu


def convertRA(ra):
    """
    Convert from decimal to sexagesimal
    From http://idlastro.gsfc.nasa.gov/ftp/pro/astro/radec.pro
    Need to put better testing in
    """
    ra1 = math.trunc(ra/15.)
    ra2 = math.trunc((ra-ra1*15.)*4)
    ra3 = ((ra-ra1*15.-ra2/4.)*240.)

    return str(ra1) + ':' + str(ra2) + ':' + str(round(ra3,6))

def convertDEC(dec):
    dec1 = math.trunc(dec)
    dec2 = math.trunc(abs(dec-dec1)*60)
    dec3 = ((abs(dec-dec1)*60.)-dec2)*60.

    return str(dec1) + ':' + str(dec2) + ':' + str(round(dec3,6))

def get_dist_mod(dist):
    " Distance should be in parsec "
    return  5*math.log10(dist) - 5

def correct_mag(c, correction):
    '''
    Add whatever correction, like a distance modulus,
    to a list of magnitudes. This function takes an
    array to correct
    '''
    return map(lambda c: c + correction , c)

def mag_cut(mag, low, high):
    """
    Define a high and low value and flag the
    values that fall within those boundaries
    """
    isGood = 0
    if mag <= high and mag >= low:
        isGood = 1
    return isGood

def color_cut(mag1, mag2, mag3, mag4, x0, x1, m, b, var):
    """
    Make color cut on a catalog based on the equation
    of a line
    """
    y_11 = gu.calcY(x1, m, b+var) # Top-right corner
    y_00 = gu.calcY(x0, m, b-var) # Lower-left corner, creates box that encompases GC locus

    px = mag1 - mag2
    py = mag3 - mag4
    if gu.inBox(x0, x1, y_00, y_11, px, py):
        return gu.inParallelogram(px, py,  m, b, var)

def det_size_cut(shape_col, bin_num):
    """
    Our size cuts are based on the thought that the
    point sources of a catalog with be clustered in
    a Gaussian distribution. This function is intended
    to return the far right value of the distribution
    in order to make the size cut.
    """
    hist, bins = np.histogram(shape_col, bin_num)
    peak =  hist.argmax()

    return round(bins[peak+10], 4)

def make_histogram(shape_col, bin_num):
    """
    Use this to check distribution of sizes values
    from SE catalogs
    """
    hist, bins = np.histogram(shape_col, bin_num)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

def calc_seeing(catalog, **kwargs):
    """
    Calculate the seeing of an image by taking a SE catalog
    cutting out the extended and dim sources and averaging
    the FWHM. Only for Subaru Suprime-Cam right now
    """
    pixel_scale = 0.20
    with open(catalog, 'r') as f:
        tmp = filter(lambda line: no_head(line), f)
        cat = map(lambda line: sources.SCAMSource(line), tmp)
    shape = map(lambda s: s.a_world, cat)
    peak = det_size_cut(shape, 1000)
    ptsources = filter(lambda s: s.a_world <= peak, cat)
    mag = map(lambda s: s.mag_best, ptsources)
    max_mag = calc_average(mag) - 3.0*calc_average(variance(mag))
    ptsources = filter(lambda s: mag_cut(s.mag_best, 0, max_mag), ptsources)
    #if kwargs['makereg']:
    fwhm = map(lambda line: line.fwhm, ptsources)
    return sum(fwhm)/len(fwhm)*pixel_scale

def calc_average(data): return sum(data)/len(data)

def variance(data):
    avg = calc_average(data)
    return map(lambda value: (value - avg)**2, data)

def calc_median(data):
    data.sort()
    if len(data) % 2 == 1:
        return data[(len(data) + 1)/2 -1]
    else:
        lower = data[len(data)/2 -1]
        upper = data[len(data)/2]
    return (float(lower + upper))/2

def calc_MAD(data):
    " Compute Median Absolute Deviation "
    med = calc_median(data)
    tmp = []
    for val in data:
        tmp.append(math.fabs(val - med))
    tmp.sort()
    return(calc_median(tmp))

def load_fits(f, **kwargs):
    if kwargs['verbose']:
        print ' ---- loading file ---- '
    __hdulist = fits.open(f)
    if kwargs['verbose']:
        __hdulist.info()
        __hdulist[0].data
        __hdulist[0].data.shape
        print ' ---- loaded file ---- '
    return __hdulist

def no_head(line):
    " Tag commented lines for easy removal "
    if line[0] != "#":
        return True
    else:
        return False

def save(path, filename, ext='png', close=True, verbose=True):
    savepath = os.path.join(path, filename)
    print savepath
    if verbose:
        print("Saving figure to '%s'..." % savepath),

    plt.savefig(savepath)

    if close:
        plt.close()

#def testColorCut():
