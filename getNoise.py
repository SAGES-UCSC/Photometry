#http://arxiv.org/pdf/1105.4609v1.pdf
#http://iopscience.iop.org/1538-3881/125/3/1107/pdf/202373.web.pdf
#http://astroa.physics.metu.edu.tr/MANUALS/sextractor/Guide2source_extractor.pdf
#http://astroa.physics.metu.edu.tr/MANUALS/sextractor/sextractor.pdf

'''
Make the call to Source Extractor with randomly generated positions.
'''

import numpy as np
import random as r
import matplotlib.pyplot as plt
import sys
import createSexConfig as sc
import createSexParam as sp
import Sources as S
import phot_utils as pu
from subprocess import call

def getNoise(aperture, name, filter_file, image,  verbose):
    x = []
    y = []
    for i in range(0,10000):
        x.append(r.uniform(1,10000))
        y.append(r.uniform(1,5000))

    output = open("MeasureFluxAt.txt", "w")
    for i in range(len(x)):
        output.write('%.3f' % x[i] + '%10.3f' % y[i]  + '\n')

    '''
    Use to check the uniformity of the coverage
    '''
    if verbose == True:
        plt.plot(x,y,linestyle='none', marker=',')
        plt.show()

    sp.createSexParam(name, True)
    assoc_file = "MeasureFluxAt.txt"
    param_file = name + ".param"

    nmad = []
    for ap in aperture:
        sc.createSexConfig(name, filter_file, param_file, assoc_file, ap, True)
        call(['sex', '-c', name + '.config', image])

        # Need to create a different parameter file
        ## I'm going to leave that and the matching until after I have more
        ## of the full program implemented
        #sc.createSexConfig()
        #call(['sex',' -c', config, image])

        '''
        Need to compare result from Source Extractor call to detection
        catalog of same image in order to reject measurments that are
        too near sources.

        Use the quadtree to speed things up once I have it working to
        match two catalogs along with three and agnostic to catalogs
        '''

        cat = open(name + ".cat")
        tmp = filter(lambda line: pu.noHead(line), cat)
        sources = map(lambda line: S.SCAMSource(line), tmp)
        flux = map(lambda s: s.mag_aper, sources)
        nmad.append(pu.calcMAD(flux))

    # Fit this plot with eq 3 from Whitaker et al
    if verbose == True:
        plt.plot(aperture, nmad, linestyle='none', marker='o')
        plt.show()

    return nmad

if __name__ == '__main__':
    sys.exit(getNoise())
