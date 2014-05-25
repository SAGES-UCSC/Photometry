'''
PURPOSE
    To calculate the zeropoint for an image
INPUT
    Aperture corrected values from the Subaru images
'''
import sys
import numpy as np
from subprocess import call
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import Quadtree as Q
import Sources as S

def associate(list1, tree2, aperture):
    dist = aperture/2
    while list1:
        target = list1.pop()
        match2 = tree2.match(target.ximg, target.yimg)
        if match2 != None and gu.norm2(match2['ra'], match2['dec'], \
                                       target.ra, target.dec) <= dist:
            target.match2 = match2

    return list1

def getSDSS(galaxy):
    " Query SDSS through Vizier "
    # Remove row limit on output table
    Vizier.ROW_LIMIT = -1
    result = Vizier.query_region("NGC4459", radius=Angle(0.1, "deg"), catalog='SDSS')

    # Only select stellar sources
    index = []
    for i, entry in enumerate(result[1]):
        if entry['cl'] != 6:
            index.append(i)
            #result[1].remove_row(i)
    result[1].remove_rows(index)

    # SDSS magnitudes are not exactly in AB so need to correct

    return result[1]

def calcZP(sdss, scam):
    # Match scam and sdss catalogs
    sdsssources = Q.VizierEquatorialQuadtree(min(sdss['RAJ2000']) - 0.1,
                                             min(sdss['DEJ2000']) - 0.1,
                                             max(sdss['RAJ2000']) + 0.1,
                                             max(sdss['DEJ2000']) + 0.1)
    map(lambda line: sdsssources.insert(line), sdss)
    matches = associate(scam, sdsssources, 4)

    ## Clip outliers of (m_sdss - m_scam)
    #std =  np.std(matches.match2['g_mag'] - m_scam.mag_aper)
    #for entries in catalog if m_sdds - m_scam > std*3 then delete entry

    ##plot to see
    #plt.plot(m_sdss - m_scam, m_scam, linestyle='none', marker=',')
    #plt.show()

    ## Take median of offset
    #return phot_utils.calcMedian()

def main():
    galaxy, scam_catalog = sys.argv[1], sys.argv[2]
    calcZP(getSDSS(galaxy), scam_catalog)


if __name__ == '__main__':
    sys.exit(main())
