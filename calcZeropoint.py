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
import Quadtree as Q
import Sources as S

def getSDSS(galaxy):
    # Query SDSS for a given galaxy and radius
    v = Vizier(columns=["**"], catalog="SDSS")
    result = v.query_region(galaxy, radius="1.0d") # Arbitray distance for now, settle on real number later
    #for entry in result[0].colnames:
    #    print entry

    # Only select stellar sources
    # This isn't working now...
    for i, entry in enumerate(result[1]):
        if entry['cl'] != '6':
            result[1].remove_row(i)

    for entry in result[1]:
        print entry['cl']

    # SDSS magnitudes are not exactly in AB so need to correct



def getSCAM(simage)

    # Use Source Extractor to get photometry

    # Do mag cut on scam data to remove saturateed sources

def calcZP():

    # Match scam and SDSS catalogs

    #plot to see
    #plt.plot(m_sdss - m_scam, m_scam, linestyle='none', marker=',')

    # Clip outliers

    # Taken median of offset

def main():


if __name__ == '__main__':
    sys.exit(main())
