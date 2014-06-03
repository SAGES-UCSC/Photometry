'''
Make a SNR plot of the ap_* files
'''

import glob
import math
import matplotlib.pyplot as plt
import numpy as np

import Sources as S
import phot_utils as pu

noisef = (glob.glob('/Users/alexawork/Documents/GlobularClusters/Photometry/NGC4649/BestApertureFiles/g_ap_*noise*txt'))
signlf = (glob.glob('/Users/alexawork/Documents/GlobularClusters/Photometry/NGC4649/BestApertureFiles/g_ap_*signal*txt'))

noise = []
for thing in noisef:
    f = open(thing)
    ntmp = map(lambda line: S.SCAMSource(line), f)
    f.close()
    nflux = map(lambda f: math.fabs(f.mag_best), ntmp)
    nflux = filter(lambda value: value != 99.0, nflux)
    noise.append(pu.calc_MAD(nflux))

signal = []
for thing in signlf:
    f = open(thing)
    stmp = map(lambda line: S.SCAMSource(line), f)
    f.close()
    sflux = map(lambda f: math.fabs(f.mag_best), stmp)
    sflux = filter(lambda value: value != 99.0, sflux)
    signal.append(pu.calc_MAD(sflux))


snr = []
#aperture = []
for i in range(len(signal)):
    snr.append(signal[i]/noise[i])
    #aperture0i.append(float(noisef[i][86:89]))
aperture = np.linspace(0.5, 12, num=5)
print snr
print aperture

plt.plot(aperture, snr, linestyle='-', marker='o', label="snr")
#plt.vlines(0.7, 0, max(snr) + 0.5, color='k', linestyles='--', label="fwhm")
#plt.plot(aperture, signal, linestyle='none', marker='o', label='signal')
#plt.plot(aperture, noise, linestyle='none', marker='o', label='noise')
plt.legend()
plt.show()
