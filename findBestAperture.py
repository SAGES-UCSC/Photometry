"""
PURPOSE
    To find the optimum aperture
"""
import sys
import numpy as np
import random as r
import math
from subprocess import call
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
        if match2 == None or gu.norm2(match2.ximg, match2.yimg, target.ximg, target.yimg) >= dist:
            unmatched.append(target)
    return unmatched

def main():
    sname = "sign"
    nname = "noise"
    image = sys.argv[1]
    filter_file = "default.conv"
    assoc_file = "MeasureFluxAt.txt"

    output = open(assoc_file, "w")
    for i in range(0,100000):
        output.write('%.3f' % r.uniform(1,11000) + '%10.3f' % r.uniform(1,9000) + '\n')

    sp.createSexParam(sname, False)
    sp.createSexParam(nname, True)
    sparam_file = sname + ".param"
    nparam_file = nname + ".param"

    signal = []
    noise = []
    aperture = np.linspace(0.5, 15, num=5)
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
        ssources = q.Quadtree(0, 0, 11000, 9000)
        map(lambda line: ssources.insert(S.SCAMSource(line)), stmp)
        nsources = map(lambda line: S.SCAMSource(line), ntmp)

        bkgddetections = disassociate(nsources, ssources, ap)
        srcdetections = map(lambda line: S.SCAMSource(line), stmp)

        output = open("ap_" + str(round(ap, 2)) + "noise.txt", "w")
        for source in bkgddetections:
            output.write(source.line)
        output = open("ap_" + str(round(ap, 2)) + "signal.txt", "w")
        for source in srcdetections:
            output.write(source.line)

if __name__ == '__main__':
    sys.exit(main())
