'''
PURPOSE
    To calculate the zeropoint for an image
INPUT
    Aperture corrected values from the Subaru images
'''
import sys
from astroquery.vizier import Vizier
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from subprocess import call
import numpy as np
import Quadtree as Q
import Sources as S
import createSexConfig as sc
import createSexParam as sp
import phot_utils

def getSDSS(galaxy):
    # Query SDSS for a given galaxy and radius
    v = Vizier(columns=["**"], catalog="SDSS")
    result = v.query_region(galaxy, radius="1.0d") # Arbitray distance for now

    # Only select stellar sources
    for i, entry in enumerate(result[1]):
        if entry['cl'] != 6:
            result[1].remove_row(i)

    # SDSS magnitudes are not exactly in AB so need to correct

    return result[1]

def getSCAM(simage, galaxy, filter_file, ap):
    # Use Source Extractor to get photometry
    sp.createSexParam(galaxy, False)
    param_file = galaxy + ".param"
    sc.createSexConfig(galaxy, filter_file, param_file, "nill", ap, False)

    call(['sex', '-c', galaxy + '.config', simage])
    with open(galaxy + '.cat', 'r') as cat:
        tmp = filter(lambda line: phot_utils.noHead(line), cat)
        sources = map(lambda line: S.SCAMSource(line), tmp)

    # Do mag cut on scam data to remove saturateed sources
    # Best way to go about this?

    # Return magntiude column
    return map(lambda source: source.mag_auto != 99.0, sources)

def calcZP(sdss, scam):
    # Match scam and sdss catalogs
    scamsources = Q.Quadtree()
    map(lambda line: scamsources.insert(line), scam)

    matches = associate()

    # Clip outliers of (m_sdss - m_scam)
    std =  np.std(m_sdss - m_scam)
    for entries in catalog if m_sdds - m_scam > std*3 then delete entry

    #plot to see
    plt.plot(m_sdss - m_scam, m_scam, linestyle='none', marker=',')
    plt.show()

    # Take median of offset
    return phot_utils.calcMedian()

def main():

    galaxy, simage = sys.argv[1], sys.argv[2]
    calcZP(getSDSS(galaxy), getSCAM(simage, galaxy, "default.conv", 4))


if __name__ == '__main__':
    sys.exit(main())
