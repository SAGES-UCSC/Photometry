#http://arxiv.org/pdf/1105.4609v1.pdf
#http://iopscience.iop.org/1538-3881/125/3/1107/pdf/202373.web.pdf
#http://astroa.physics.metu.edu.tr/MANUALS/sextractor/Guide2source_extractor.pdf
#http://astroa.physics.metu.edu.tr/MANUALS/sextractor/sextractor.pdf

import numpy as np
import random as r
import matplotlib.pyplot as plt
import sys
import createSexConfig as sc
import Sources as S
import phot_utils as pu
from subprocess import call


def main():
    '''
    Generating a textfile of random positions
    '''
    #x = []
    #y = []
    #for i in range(0,1000000):
    #    x.append(r.uniform(1,10000))
    #    y.append(r.uniform(1,5000))

    #output = open("MeasureFluxAt.txt", "w")
    #for i in range(len(x)):
    #    output.write('%.3f' % x[i] + '%10.3f' % y[i]  + '\n')

    '''
    Can be used as a check on the uniformity of the coverage
    if you're worried about that sort of thing
    '''
    #plt.plot(x,y,linestyle='none', marker=',')
    #plt.show()

    aperture = np.linspace(0.5, 10, num=10)
    nmad = []
    for ap in aperture:
        '''
        Make the call to Source Extractor with randomly generated positions.
        And then do it again but this time just to get detections
        '''
        image      = "NGC4374_i.fits"
        assoc_file = "MeasureFluxAt.txt"
        param_file  = "gc_select.param"
        filter_file     = "default.conv"
        name = "blargh"

        config = sc.createSexConfig(name, filter_file, param_file, assoc_file, ap)
        call(['sex', '-c', 'blargh.config', image])

        ## Need to figure out a way in createSexConfig to switch off ASSOC
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

        '''
        Calculate NMAD value for this aperture size. Save to array
        '''
        cat = open("blargh.cat")
        tmp = filter(lambda line: pu.noHead(line), cat)
        sources = map(lambda line: S.SCAMSource(line), tmp)
        flux = map(lambda s: s.mag_aper, sources)
        nmad.append(pu.calcMAD(flux))

    plt.plot(aperture, nmad, linestyle='none', marker='o')
    plt.show()

if __name__ == '__main__':
    sys.exit(main())
