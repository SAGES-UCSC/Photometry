import sys
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import Quadtree as Q
import Sources as S
import phot_utils
import geom_utils

def associate(table, tree2):
    dist = 0.04
    matches = []
    for entry in table:
        match = tree2.match(entry['RAJ2000'], entry['DEJ2000'])
        if match != None and geom_utils.equnorm(entry['RAJ2000'], entry['DEJ2000'], \
                                       match.ra, match.dec) <= dist:
            match.match2 = entry
            matches.append(match)
    return matches

def getSDSS(galaxy):
    """
    Query SDSS through Vizier, pick out only the stellar sources,
    and put the SDSS magnitudes into AB
    """
    Vizier.ROW_LIMIT = -1 # Removes row limit on output table
    result = Vizier.query_region(galaxy, radius=Angle(0.1, "deg"), catalog='SDSS')
    # Only select stellar sources
    index = []
    for i, entry in enumerate(result[1]):
        if entry['cl'] != 6:
            index.append(i)
    result[1].remove_rows(index)

    # SDSS magnitudes are not exactly in AB so need to correct
    return result[1]

def calcZP(sdss, scam):
    """
    To calculate the zeropoint of the Subaru image match the Subaru catalog
    and the table returned from Vizier.
    """
    with open(scam, 'r') as catalog:
        tmp = filter(lambda line: phot_utils.no_head(line), catalog)
    # Do magnitude cute on data here
    tmp2 = map(lambda line: S.SCAMSource(line), tmp)
    mag = map(lambda s: s.mag_best, tmp2)
    max_mag = phot_utils.calc_average(mag) + 0.25*phot_utils.calc_average(phot_utils.variance(mag))
    sources = filter(lambda s: phot_utils.mag_cut(s.mag_best, 0, max_mag), tmp2)


    ra = map(lambda line: line.ra, tmp2)
    dec = map(lambda line: line.dec, tmp2)
    scam_sources = Q.ScamEquatorialQuadtree(min(ra), min(dec),
                                            max(ra), max(dec))
    map(lambda sources: scam_sources.insert(sources), sources)
    matches = associate(sdss, scam_sources)

    m_scam = map(lambda source: source.mag_aper, matches)
    m_sdss = map(lambda source: source.match2['gmag'], matches)

    # Clip outliers of (m_sdss - m_scam)
    difference = []
    for i, entry in enumerate(m_scam):
        difference.append(m_sdss[i] - m_scam[i])
    std =  np.std(difference)
    print "Standard Deviation of Difference Magnitudes: ", std

    clipped = []
    for entry in matches:
        if entry.match2['gmag'] - entry.mag_aper < std*3:
            clipped.append(entry)

    difference = []
    for entry in clipped:
        difference.append(entry.match2['gmag'] - entry.mag_aper)
    m_scam = map(lambda source: source.mag_aper, clipped)

    # Look at offsets
    plt.plot(difference, m_scam, linestyle='none', marker='o')
    plt.xlabel(r'$m_{SDSS}$ - $m_{SCAM}$', fontsize=20)
    plt.ylabel(r'$m_{SCAM}$', fontsize=20, labelpad=30)
    plt.show()

    # Take median of offset
    return  phot_utils.calcMedian(difference)

def main():
    galaxy, scam_catalog = sys.argv[1], sys.argv[2]
    calcZP(getSDSS(galaxy), scam_catalog)


if __name__ == '__main__':
    sys.exit(main())
