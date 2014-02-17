"""
PURPOSE
    To find the optimum aperture
"""
import sys
import numpy as np
import random as r
import getNoise as gn
import createSexConfig as sc
import createSexParam as sp
import phot_utils as pu
import Sources as S
import matplotlib.pyplot as plt
from subprocess import call
import Quadtree as q
from pprint import pprint
import geom_utils as gu

MAXDIST = 2

'''
In this case we want the objects that DON'T match
'''
def disassociate(list1, tree2):
    unmatched = []
    while list1:
        target = list1.pop()
        match2 = tree2.match(target.ximg, target.yimg)
        if match2 != None and gu.norm2(match2.ximg, match2.yimg, target.ximg, target.yimg) > MAXDIST:
            target.match2 = match2
            unmatched.append(target)

    return unmatched

def main():
    sname = "sign"
    nname = "noise"
    image = "NGC4374_i.fits"
    filter_file = "default.conv"

    output = open("MeasureFluxAt.txt", "w")
    for i in range(0,100000):
        output.write('%.3f' % r.uniform(1,10000) + '%10.3f' % r.uniform(1,8000) + '\n')

    sp.createSexParam(sname, False)
    sp.createSexParam(nname, True)
    sparam_file = sname + ".param"
    nparam_file = nname + ".param"
    assoc_file = "MeasureFluxAt.txt"

    signal = []
    noise = []
    aperture = np.linspace(0.5, 15, num=20)
    for ap in aperture:
        sc.createSexConfig(sname, filter_file, sparam_file, "nill", ap, False)
        call(['sex', '-c', sname + '.config', image])

        sc.createSexConfig(nname, filter_file, nparam_file, assoc_file, ap, True)
        call(['sex', '-c', nname + '.config', image])

        scat = open(sname + ".cat")
        stmp = filter(lambda line: pu.noHead(line), scat)

        ncat = open(nname + ".cat")
        ntmp = filter(lambda line: pu.noHead(line), ncat)

        # Background measuresments can't overlap with source detections
        # Also don't include mag_aper == 99.0
        ssources = q.Quadtree(0, 0, 11000, 9000)
        map(lambda line: ssources.insert(S.SCAMSource(line)), stmp)
        nsources = map(lambda line: S.SCAMSource(line), ntmp)

        bkgddetections = disassociate(nsources, ssources)
        srcdetections = map(lambda line: S.SCAMSource(line), stmp)

        print "For ", ap, "there are ", len(bkgddetections)

        sflux = map(lambda s: s.mag_aper, srcdetections)
        signal.append(pu.calcMAD(sflux))

        nflux = map(lambda s: s.mag_aper, bkgddetections)
        noise.append(pu.calcMAD(nflux))

        output = open("ap_" + str(ap) + "noise.txt")
        for source in bkgddetections:
            output.write(source.line)
        output = open("ap_" + str(ap) + "signal.txt")
        for source in srcdetections:
            output.write(source.line)

    snr = []
    for i in range(len(signal)):
        snr.append(signal[i]/noise[i])

    plt.plot(aperture, snr, linestyle='none', marker='o')
    plt.show()
    plt.plot(aperture, signal, linestyle='none', marker='o')
    plt.show()
    plt.plot(aperture, noise, linestyle='none', marker='o')
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
