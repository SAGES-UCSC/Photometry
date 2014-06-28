"""
PURPOSE
    To find the optimum aperture for an image
"""
import sys
import numpy as np
import os
import random as r
import math
from subprocess import call
import matplotlib.pyplot as plt
import glob
import time

import createSexConfig as sc
import createSexParam as sp
import phot_utils as pu
import Sources as S
import matplotlib.pyplot as plt
import Quadtree as q
import geom_utils as gu

'''
In this case we want the objects that DON'T match
'''
def disassociate(list1, tree2, aperture):
    dist = aperture/2
    unmatched = []
    while list1:
        target = list1.pop()
        match2 = tree2.match(target.ximg, target.yimg)
        if match2 == None or gu.pixnorm(match2.ximg, match2.yimg, target.ximg, target.yimg) >= dist:
            unmatched.append(target)
    return unmatched

def findBestAperture(path, image, satur, seeing):
    if os.path.isdir('BestApertureFiles') == False:
        os.mkdir('BestApertureFiles')

    sname = "sign"
    nname = "noise"
    filter_file = "default.conv"
    assoc_file = "measurefluxat.txt"

    output = open(assoc_file, "w")
    for i in xrange(0,100000):
        output.write('%.3f' % r.uniform(1,11000) + '%10.3f' % r.uniform(1,9000) + '\n')

    sp.createSexParam(sname, False)
    sp.createSexParam(nname, True)
    sparam_file = sname + ".param"
    nparam_file = nname + ".param"

    signal = []
    noise = []
    aperture = np.linspace(0.5, 12, num=10)
    for ap in aperture:
        sc.createSexConfig(sname, filter_file, sparam_file, satur, seeing, "nill", ap, False)
        call(['sex', '-c', sname + '.config', image])
        sc.createSexConfig(nname, filter_file, nparam_file, satur, seeing, assoc_file, ap, True)
        call(['sex', '-c', nname + '.config', image])

        scat = open(sname + ".cat")
        stmp = filter(lambda line: pu.no_head(line), scat)
        ncat = open(nname + ".cat")
        ntmp = filter(lambda line: pu.no_head(line), ncat)

        # Background measuresments can't overlap with source detections
        ssources = q.ScamPixelQuadtree(0, 0, 12000, 10000)
        map(lambda line: ssources.insert(S.SCAMSource(line)), stmp)
        nsources = map(lambda line: S.SCAMSource(line), ntmp)

        start = time.time()
        bkgddetections = disassociate(nsources, ssources, ap)
        end = time.time()
        print("ELAPSED TIME: " + str(end-start))
        srcdetections = map(lambda line: S.SCAMSource(line), stmp)

        flux = map(lambda f: f.flux_aper, bkgddetections)
        noise.append(pu.calc_MAD(flux))

        flux = map(lambda f: f.flux_aper, srcdetections)
        signal.append(pu.calc_MAD(flux))

        with open(image[-6] + "_ap_" + str(round(ap, 2)) + "noise.txt", "w") as output:
            for source in bkgddetections:
                output.write(source.line)
        call(['mv', image[-6] + "_ap_" + str(round(ap, 2)) + "noise.txt", 'BestApertureFiles'])

        with open(image[-6] + "_ap_" + str(round(ap, 2)) + "signal.txt", "w") as output:
            for source in srcdetections:
                output.write(source.line)
        call(['mv', image[-6] + "_ap_" + str(round(ap, 2)) + "signal.txt", 'BestApertureFiles'])

    '''
    The files generated here aren't important and need to be
    removed for the next steps to work properly.
    '''

    try:
        os.remove('measurefluxat.txt')
    except OSError:
        pass
    noise_files = (glob.glob('noise*'))
    try:
        for f in noise_files:
            os.remove(f)
    except OSError:
        pass
    sign_files = (glob.glob('sign*'))
    try:
        for f in sign_files:
            os.remove(f)
    except OSError:
        pass

    snr = []
    for i in range(len(noise)):
        snr.append(signal[i]/noise[i])
    plt.plot(aperture, snr, linestyle='none', marker='o')
    plt.xlabel('Aperture (pix)')
    plt.ylabel('SNR')
    pu.save(path, image[-6]+'_snr')
    maxsnr = snr.index(max(snr))
    return aperture[maxsnr]

if __name__ == '__main__':
    sys.exit(main())
