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

    # Do mag cut on scam data to remove saturateed sources

def calcZP():
    print 'blaah'
    # Match scam and SDSS catalogs

    #plot to see
    #plt.plot(m_sdss - m_scam, m_scam, linestyle='none', marker=',')

    # Clip outliers

    # Taken median of offset

def main():

    galaxy, simage = sys.argv[1], sys.argv[2]
    getSDSS(galaxy)
    getSCAM(simage, galaxy, "default.conv", 4)

if __name__ == '__main__':
    sys.exit(main())
