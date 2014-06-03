'''
Determine optimum aperture and use Source Extractor to get photometry
'''
import sys
import os
from subprocess import call, Popen, PIPE
import glob

import Sources as sources
import createSexConfig
import createSexParam
import findBestAperture
import phot_utils
import geom_utils

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
        image = phot_utils.load_fits(img, verbose=False)
        satur = image[0].header['SATURATE']
        seeing = 1
        ap = findBestAperture.findBestAperture(img, satur, seeing)
        fname = system + '_' + img[-6]
        # Extract sources with initial rough estimate of seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing, "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])
        seeing = phot_utils.calc_seeing(fname + '.cat')

        # Re-extract with refined seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing, "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])

        # Re-name the check images created
        checks = (glob.glob('*.fits'))
        for check in checks:
            os.rename(check, fname + '_' + check)

if __name__ == '__main__':
    sys.exit(main())

