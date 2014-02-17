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

MAXDIST = 0

'''
In this case we want the objects that DON'T match
'''
def disassociate(list1, tree2):
    unmatched = []
    while list1:
        target = list1.pop()
        match2 = tree2.match(target.ximg, target.yimg)
        if match2 != None and norm2(match2.ximg, match2.yimg, target.ximg, target.yimg) > MAXDIST:
            print target
            unmatched.append(target)

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
    aperture = np.linspace(0.5, 10, num=1)
    for ap in aperture:
#        sc.createSexConfig(sname, filter_file, sparam_file, "nill", ap, False)
#        call(['sex', '-c', sname + '.config', image])

#        sc.createSexConfig(nname, filter_file, nparam_file, assoc_file, ap, True)
#        call(['sex', '-c', nname + '.config', image])

        scat = open(sname + ".cat")
        stmp = filter(lambda line: pu.noHead(line), scat)

        ncat = open(nname + ".cat")
        ntmp = filter(lambda line: pu.noHead(line), ncat)

        # Background measuresments can't overlap with source detections
        # Also don't include mag_aper == 99.0
        ssources = q.Quadtree(0, 0, 11000, 9000)
        for i in range(0,13):
            ssources.insert(S.SCAMSource(stmp[i]))
#        map(lambda line: ssources.insert(S.SCAMSource(line)), stmp)
        nsources = map(lambda line: S.SCAMSource(line), ntmp)

        bkgddetections = disassociate(nsources, ssources)

        #sflux = map(lambda s: s.mag_aper, ssources)
        #signal.append(pu.calcMAD(sflux))

        #nflux = map(lambda s: s.mag_aper, bkgddetections)
        #noise.append(pu.calcMAD(nflux))


#    snr = []
#    for i in range(len(signal)):
#        snr.append(signal[i]/noise[i])

#    plt.plot(aperture, sflux, linestyle='none', marker='o')
#    plt.plot(aperture, nflux, linestyle='none', marker='o')
#    plt.show()

if __name__ == '__main__':
    sys.exit(main())


