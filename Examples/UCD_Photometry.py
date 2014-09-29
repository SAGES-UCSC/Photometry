'''
Determine optimum aperture and use Source Extractor to get photometry
'''
import sys
import os
from subprocess import call, Popen, PIPE
import glob
import math
import numpy as np

import Sources
import Quadtree
import createSexConfig
import createSexParam
import findBestAperture
import calcZeropoint
import makeRegionFile
import phot_utils
import geom_utils

verbose=True

def associate(list1, tree2, tree3):
    dist = 0.001
    matches = []
    for entry in list1:
        match2 = tree2.match(entry.ra, entry.dec)
        if match2 != None and geom_utils.equnorm(entry.ra, entry.dec, match.ra, match.dec) <= dist:
            match3 = tree3.match(entry.ra, entry.dec)
            if match3 != None and geom_utils.equnorm(entry.ra, entry.dec, match3.ra, match3.dec) <= dist:
                # Match2 is r-magnitudes
                entry.match2 = match2.mag_aper
                # Match3 is i-magnitudes
                entry.match3 = match3.mag_aper
                matches.append(entry)
    return matches

def get_photometry(system, in_images):
    subs= []
    imgs = []
    with(open(in_images, "r")) as f:
        for line in f:
            cols = line.split()
            subs.append(cols[0])
            imgs.append(cols[1])

    filter_file = "default.conv"
    param_file = createSexParam.createSexParam(system, False)

    path = '/Users/alexawork/Documents/GlobularClusters/Data/NGC4621'
    for galsub, img in zip(subs, imgs):
        image = phot_utils.load_fits(img, verbose=False)
        path = os.getcwd()
        fname = system + '_' + img[-6]
        seeing = [1, 1]
        satur = image[0].header['SATURATE']
        #ap = findBestAperture.findBestAperture(path, img, satur, seeing[0])
        ap = 5
        # Extract sources with initial rough estimate of seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing[0], "nill", ap, False)
        call(['sex', '-c', config, galsub, img])

        seeing = phot_utils.calc_seeing(fname + '.cat', verbose=verbose)
        "If the aperture is less than the seeing round it up to next interger"
        if ap < seeing[1]:
            ap = math.ceil(seeing[1])
        # Re-extract with refined seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing[0], "nill", ap, False)
        call(['sex', '-c', config, galsub, img])

        # Re-name the check images created
        checks = (glob.glob('*.fits'))
        if not os.path.isdir('CheckImages'):
            os.mkdir('CheckImages')
        for check in checks:
            os.rename(check, fname + '_' + check)
            call(['mv', fname + '_' + check, 'CheckImages'])

def correct_mags(galaxy, catalog, band):
    print "band: ", band
    zp = calcZeropoint.calcZP(galaxy, catalog, band)
    if verbose:
        print "Zeropoint for " + band + "-band", zp

    with open(catalog, 'r') as f:
        tmp = filter(lambda line: phot_utils.no_head(line), f)

    sources = map(lambda line: Sources.SCAMSource(line), tmp)
    for source in sources:
        source.mag_aper = round(source.mag_aper + zp, 3)
        source.mag_auto = round(source.mag_auto + zp, 3)
        source.mag_best = round(source.mag_best + zp, 3)

    new_catalog = 'zpcorrected_' + catalog
    with open(new_catalog, 'w') as output:
        output.write(''.join(map(lambda source: '%5s' % source.name + '%15s' % source.flux_iso +
                    '%15s' % source.fluxerr_iso + '%15s' % source.flux_aper +
                    '%15s' % source.fluxerr_aper + '%15s' % source.ximg + '%15s' % source.yimg +
                    '%15s' % source.ra + '%15s' % source.dec + '%15s' % source.mag_auto +
                    '%15s' % source.mag_auto_err + '%15s' % source.mag_best +
                    '%15s' % source.mag_best_err + '%15s' % source.mag_aper +
                    '%15s' % source.mag_aper_err + '%15s' % source.a_world +
                    '%15s' % source.a_world_err + '%15s' % source.b_world +
                    '%15s' % source.b_world_err + '%15s' % source.theta_err +
                    '%15s' % source.theta + '%15s' % source.isoarea + '%15s' % source.mu +
                    '%15s' % source.flux_radius + '%15s' % source.flags + '%15s' % source.fwhm +
                    '%15s' % source.elogation + '%15s' % source.vignet + '\n',  sources)))
    return new_catalog

def make_trees(catalog):
    with open(catalog, 'r') as f:
        tmp = filter(lambda line: phot_utils.no_head(line), f)
    tmp2 = map(lambda line: Sources.SCAMSource(line), tmp)

    ra = map(lambda line: line.ra, tmp2)
    dec = map(lambda line: line.dec, tmp2)
    sources = Quadtree.ScamEquatorialQuadtree(min(ra), min(dec),
                                              max(ra), max(dec))
    map(lambda line: sources.insert(line), tmp2)

    #if verbose:
    #        makeRegionFile.makeRegionFile('NGC4621_i.cat', 'NGC4621_i.reg', 10, 'blue')

    return sources

def main():
#    get_photometry(sys.argv[1], sys.argv[2])
#    catalogs = (glob.glob('NGC4621*.cat'))
#    for catalog in catalogs:
#        if verbose:
#            print "Working on catalog: ", catalog
#        corrected_catalog = correct_mags(sys.argv[1], catalog, catalog[-5])


    catalogs = (glob.glob('zpcorrected*.cat'))
    trees = {}
    for catalog in catalogs:
        trees[catalog[-5]] = make_trees(catalog)

    m59_ucd3_i = trees['i'].match(190.54601, 11.64478)
    m59_ucd3_g = trees['g'].match(190.54601, 11.64478)
    m59_ucd3_r = trees['r'].match(190.54601, 11.64478)

    print '\n'

    print "M59-UCD3's Location in catalog: ", m59_ucd3_i.name
    print 'MAG_AUTO: '
    print "I Mag and G Mag: ",  m59_ucd3_i.mag_auto, m59_ucd3_g.mag_auto
    print 'M59-UCD3 g-i: ', m59_ucd3_g.mag_auto - m59_ucd3_i.mag_auto
    print 'MAG_APER: '
    print "I Mag and G Mag: ",  m59_ucd3_i.mag_aper, m59_ucd3_g.mag_aper
    print 'M59-UCD3 g-i: ', m59_ucd3_g.mag_aper - m59_ucd3_i.mag_aper
    print 'M59-UCD3 FWHM: ', m59_ucd3_g.fwhm*0.2
    print 'M59_UCD3 Half-Light Radius: ', m59_ucd3_g.flux_radius
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59_ucd3_i.ra), phot_utils.convertDEC(m59_ucd3_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59_ucd3_g.ra), phot_utils.convertDEC(m59_ucd3_g.dec)

    print '\n'
    print '\n'

    m59cO_i = trees['i'].match(190.48056, 11.66771)
    m59cO_g = trees['g'].match(190.48056, 11.66771)
    m59cO_r = trees['r'].match(190.48056, 11.66771)

    print "M59cO's Location in catalog: ", m59cO_i.name
    print "MAG_AUTO: "
    print "I Mag and G Mag: ", m59cO_i.mag_auto, m59cO_g.mag_auto
    print 'M59cO g-i: ', m59cO_g.mag_auto - m59cO_i.mag_auto
    print "MAG_APER: "
    print "I Mag and G Mag: ", m59cO_i.mag_aper, m59cO_g.mag_aper
    print 'M59cO g-i: ', m59cO_g.mag_aper - m59cO_i.mag_aper
    print 'M59cO Half-Light Radius: ', m59cO_g.flux_radius
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59cO_i.ra), phot_utils.convertDEC(m59cO_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59cO_g.ra), phot_utils.convertDEC(m59cO_g.dec)

    print '\n'
    print '\n'

    m59_gcx_i = trees['i'].match(190.50245, 11.65993)
    m59_gcx_g = trees['g'].match(190.50245, 11.65993)
    m59_gcx_r = trees['r'].match(190.50245, 11.65993)

    print "M59_gcx's Location in catalog: ", m59cO_i.name
    print "MAG_AUTO: "
    print "I Mag and G Mag: ", m59cO_i.mag_auto, m59cO_g.mag_auto
    print 'M59_gcx g-i: ', m59cO_g.mag_auto - m59cO_i.mag_auto
    print "MAG_APER: "
    print "I Mag and G Mag: ", m59cO_i.mag_aper, m59cO_g.mag_aper
    print 'M59_gcx g-i: ', m59cO_g.mag_aper - m59cO_i.mag_aper
    print 'M59_gcx Half-Light Radius: ', m59cO_g.flux_radius
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59cO_i.ra), phot_utils.convertDEC(m59cO_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59cO_g.ra), phot_utils.convertDEC(m59cO_g.dec)

    print '\n'
    print '\n'

    m59_gcy_i = trees['i'].match(190.51231, 11.63986)
    m59_gcy_g = trees['g'].match(190.51231, 11.63986)
    m59_gcy_r = trees['r'].match(190.51231, 11.63986)

    print "M59_gcy's Location in catalog: ", m59cO_i.name
    print "MAG_AUTO: "
    print "I Mag and G Mag: ", m59cO_i.mag_auto, m59cO_g.mag_auto
    print 'M59_gcy g-i: ', m59cO_g.mag_auto - m59cO_i.mag_auto
    print "MAG_APER: "
    print "I Mag and G Mag: ", m59cO_i.mag_aper, m59cO_g.mag_aper
    print 'M59_gcy g-i: ', m59cO_g.mag_aper - m59cO_i.mag_aper
    print 'M59_gcy Half-Light Radius: ', m59cO_g.flux_radius
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59cO_i.ra), phot_utils.convertDEC(m59cO_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59cO_g.ra), phot_utils.convertDEC(m59cO_g.dec)

    print '\n'
    print '\n'

    ngc_4621_aimss1_i = trees['i'].match(190.47050, 11.63001)
    ngc_4621_aimss1_g = trees['g'].match(190.47050, 11.63001)
    ngc_4621_aimss1_r = trees['r'].match(190.47050, 11.63001)

    print "ngc_4621_aimss's Location in catalog: ", m59cO_i.name
    print "MAG_AUTO: "
    print "I Mag and G Mag: ", m59cO_i.mag_auto, m59cO_g.mag_auto
    print 'ngc_4621_aimss g-i: ', m59cO_g.mag_auto - m59cO_i.mag_auto
    print "MAG_APER: "
    print "I Mag and G Mag: ", m59cO_i.mag_aper, m59cO_g.mag_aper
    print 'ngc_4621_aimss g-i: ', m59cO_g.mag_aper - m59cO_i.mag_aper
    print 'ngc_4621_aimss Half-Light Radius: ', m59cO_g.flux_radius
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59cO_i.ra), phot_utils.convertDEC(m59cO_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59cO_g.ra), phot_utils.convertDEC(m59cO_g.dec)

    print '\n'
    print '\n'


#    with open('NGC4621_g.cat', 'r') as catalog:
#        tmp = filter(lambda line: phot_utils.no_head(line), catalog)
#    g_sources = map(lambda source: Sources.SCAMSource(source), tmp)
#
#    r_sources = make_trees('NGC4621_r.cat')
#    i_sources = make_trees('NGC4621_i.cat')
#
#    matches = associate(g_sources, r_sources, i_sources)
#
#    with open('matched_gri.cat', 'w') as out:
#        out.write()

if __name__ == '__main__':
    sys.exit(main())

