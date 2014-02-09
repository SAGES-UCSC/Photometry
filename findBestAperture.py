"""
PURPOSE
    To find the optimum aperture
"""
import sys
import numpy as np
import getNoise as gn
import createSexConfig as sc
import createSexParam as sp
import phot_utils as pu
import Sources as S
import matplotlib.pyplot as plt
from subprocess import call

def main():
    name        = "blargh"
    image       = "NGC4374_i.fits"
    assoc_file  = "MeasureFluxAt.txt"
    param_file  = "gc_select.param"
    filter_file = "default.conv"

    aperture = np.linspace(0.5, 10, num=5)
    noise = gn.getNoise(aperture, name, filter_file, image,  False)

    sp.createSexParam(name, False)
    param_file = name + ".param"

    signal = []
    for ap in aperture:
        sc.createSexConfig(name, filter_file, param_file, assoc_file, ap, False)
        call(['sex', '-c', name + '.config', image])

        cat = open("blargh.cat")
        tmp = filter(lambda line: pu.noHead(line), cat)
        sources = map(lambda line: S.SCAMSource(line), tmp)
        flux = map(lambda s: s.mag_aper, sources)
        signal.append(pu.calcMAD(flux))

    snr = []
    for i in range(len(signal)):
        snr.append(signal[i]/noise[i])

    plt.plot(aperture, snr, linestyle='none', marker='o')
    plt.show()

if __name__ == '__main__':
    sys.exit(main())


