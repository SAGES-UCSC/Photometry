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

def main():

    # Query SDSS for a given galaxy and radius
    v = Vizier(columns=["**"], catalog="SDSS")
    result = v.query_region("NGC3377", radius="1.0d") # Arbitray distance for now, settle on real number later
    #for entry in result[0].colnames:
    #    print entry

    # Only select stellar sources
    # This seems to make the table messy to handle. Try something else
    stars = filter(lambda line: line['cl'] == 6, result[1])

    # SDSS magnitudes are not exactly in AB so need to correct


    # Do mag cut on scam data to remove saturateed sources


    # Match scam and SDSS catalogs

    #plot to see
    #plt.plot(m_sdss - m_scam, m_scam, linestyle='none', marker=',')

    # Clip outliers

    # Taken median of offset


if __name__ == '__main__':
    sys.exit(main())
