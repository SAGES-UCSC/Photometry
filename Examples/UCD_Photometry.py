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

verbose=False

def get_photometry(system, in_images):
    galsub = []
    imgs = []
    with(open(in_images, "r")) as f:
        for line in f:
            cols = line.split()
            galsub.append(cols[0])
            imgs.append(cols[1])

    filter_file = "default.conv"
    param_file = createSexParam.createSexParam(system, False)

    for i, img in enumerate(imgs):
        image = phot_utils.load_fits(img, verbose=False)
        satur = image[0].header['SATURATE']
        seeing = 1
        path = os.getcwd()
        fname = system + '_' + img[-12]
        ap = findBestAperture.findBestAperture(path, img, satur, seeing)
        # Extract sources with initial rough estimate of seeing
        seeing = [1, 1]
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing[0], "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])

        seeing = phot_utils.calc_seeing(fname + '.cat', verbose=verbose)
        "If the aperture is less than the seeing round it up to next interger"
        if ap < seeing[1]:
            ap = math.ceil(ap)
        # Re_extract with refined seeing
        config = createSexConfig.createSexConfig(fname, filter_file,
                 param_file, satur, seeing[0], "nill", ap, False)
        call(['sex', '-c', config, galsub[i], img])

        # Re-name the check images created
        checks = (glob.glob('*.fits'))
        if not os.path.isdir('CheckImages'):
            os.mkdir('CheckImages')
        for check in checks:
            os.rename(check, fname + '_' + check)
            call(['mv', fname + '_' + check, 'CheckImages'])

def correct_mags(galaxy, catalog, band):
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

    if verbose:
            makeRegionFile.makeRegionFile('NGC4621_i.cat', 'NGC4621_i.reg', 10, 'blue')

    return sources

def main():
    #get_photometry(sys.argv[1], sys.argv[2])
    catalogs = (glob.glob('*.cat'))
    trees = {}
    for catalog in catalogs:
        if verbose:
            print "Working on catalog: ", catalog
        corrected_catalog = correct_mags(sys.argv[1], catalog, catalog[-5])
        trees[catalog[-5]] = make_trees(corrected_catalog)

    # Aaron gave me the coordinates
    m59_ucd3_i = trees['i'].match(190.54601, 11.64478)
    m59_ucd3_g = trees['g'].match(190.54601, 11.64478)

    print '\n'

    print "M58-UCD3's Location in catalog: ", m59_ucd3_i.name
    print 'MAG_AUTO: '
    print "I Mag and G Mag: ",  m59_ucd3_i.mag_auto, m59_ucd3_g.mag_auto
    print 'M59-UCD3 g-i: ', m59_ucd3_g.mag_auto - m59_ucd3_i.mag_auto
    print 'MAG_APER: '
    print "I Mag and G Mag: ",  m59_ucd3_i.mag_aper, m59_ucd3_g.mag_aper
    print 'M59-UCD3 g-i: ', m59_ucd3_g.mag_aper - m59_ucd3_i.mag_aper
    print 'M59-UCD3 FWHM: ', m59_ucd3_g.fwhm*0.2
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59_ucd3_i.ra), phot_utils.convertDEC(m59_ucd3_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59_ucd3_g.ra), phot_utils.convertDEC(m59_ucd3_g.dec)

    print '\n'
    print '\n'

    m59cO_i = trees['i'].match(190.48056, 11.66771)
    m59cO_g = trees['g'].match(190.48056, 11.66771)
    print "M59cO's Location in catalog: ", m59cO_i.name
    print "MAG_AUTO: "
    print "I Mag and G Mag: ", m59cO_i.mag_auto, m59cO_g.mag_auto
    print 'M59cO g-i: ', m59cO_g.mag_auto - m59cO_i.mag_auto
    print "MAG_APER: "
    print "I Mag and G Mag: ", m59cO_i.mag_aper, m59cO_g.mag_aper
    print 'M59cO g-i: ', m59cO_g.mag_aper - m59cO_i.mag_aper
    print "Coordinates from i-band catalog - "
    print phot_utils.convertRA(m59cO_i.ra), phot_utils.convertDEC(m59cO_i.dec)
    print "Coordinates from g-band catalog - "
    print phot_utils.convertRA(m59cO_g.ra), phot_utils.convertDEC(m59cO_g.dec)

    print '\n'

    #M59_GCX = sources.match(190.50245, 11.65993)
    #print M59_GCX.name
    #print phot_utils.convertRA(M59_GCX.ra), phot_utils.convertDEC(M59_GCX.dec)

    #M59_GCY = sources.match(190.51231, 11.63986)
    #print M59_GCY.name
    #print phot_utils.convertRA(M59_GCY.ra), phot_utils.convertDEC(M59_GCY.dec)

    #NGC_4621_AIMSS1 = sources.match(190.47050, 11.63001)
    #print NGC_4621_AIMSS1.name
    #print phot_utils.convertRA(NGC_4621_AIMSS1.ra), phot_utils.convertDEC(NGC_4621_AIMSS1.dec)

if __name__ == '__main__':
    sys.exit(main())

