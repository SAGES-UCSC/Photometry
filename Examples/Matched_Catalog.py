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

    if verbose:
            makeRegionFile.makeRegionFile('NGC4621_i.cat', 'NGC4621_i.reg', 10, 'blue')

    return sources

def main():
    #get_photometry(sys.argv[1], sys.argv[2])
    catalogs = (glob.glob('NGC4621*.cat'))
    for catalog in catalogs:
        if verbose:
            print "Working on catalog: ", catalog
        corrected_catalog = correct_mags(sys.argv[1], catalog, catalog[-5])

    sys.exit()

    with open('NGC4621_g.cat', 'r') as catalog:
        tmp = filter(lambda line: phot_utils.no_head(line), catalog)
    g_sources = map(lambda source: Sources.SCAMSource(source), tmp)

    r_sources = make_trees('NGC4621_r.cat')
    i_sources = make_trees('NGC4621_i.cat')

    matches = associate(g_sources, r_sources, i_sources)

    with open('matched_gri.cat', 'w') as out:
        out.write()

if __name__ == '__main__':
    sys.exit(main())

