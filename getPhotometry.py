'''
Determine optimum aperture and use Source Extractor to get photometry
'''
import sys
import os
from subprocess import call, Popen, PIPE
from astropy.io import fits
import glob

import Sources as sources
import createSexConfig
import createSexParam
import findBestAperture
import phot_utils
import geom_utils

def load_file(f, **kwargs):
    if kwargs['verbose']:
        print ' ---- loading file ---- '
    __hdulist = fits.open(f)
    if kwargs['verbose']:
        __hdulist.info()
        __hdulist[0].data
        __hdulist[0].data.shape
        print ' ---- loaded file ---- '
    return __hdulist

def calc_seeing(catalog):
    with open(catalog, 'r') as f:
        tmp = filter(lambda line: phot_utils.noHead(line), f)
        cat = map(lambda line: sources.SCAMSource(line), tmp)
    # Make shape and brightness cut so only using the best
    # point sources
    shape = map(lambda s: s.a_world, cat)
    peak = phot_utils.detSizeCut(shape, 1000)
    ptsources = filter(lambda s: s.a_world <= peak, cat)
    ptsources = filter(lambda s: s.mag_aper <= 20, ptsources)
    # Find the average FWHM and multiply it by the Suprime-Cam
    # pixel scale to put it in arcsec
    fwhm = map(lambda line: line.fwhm, ptsources)
    return sum(fwhm)/len(fwhm)*0.20

def main():
    system = sys.argv[1]
    galsub = []
    imgs = []
    with(open(sys.argv[2], "r")) as f:
        for line in f:
            cols = line.split()
            galsub.append(cols[0])
            imgs.append(cols[1])

    filter_file = "default.conv"
    param_file = createSexParam.createSexParam(system, False)

    for i, img in enumerate(imgs):
        image = load_file(img, verbose=False)
        satur = image[0].header['SATURATE']
        seeing = 1
        ap = findBestAperture.findBestAperture(img, satur, seeing)
        fname = system + '_' + img[-6]
        # Extract sources with initial rough estimate of seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing, "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])
        seeing = calc_seeing(fname + '.cat')

        # Re-extract with refined seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing, "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])

        # Re-name the check images created
        checks = (glob.glob('*.fits'))
        for check in checks:
            os.rename(check,

if __name__ == '__main__':
    sys.exit(main())

