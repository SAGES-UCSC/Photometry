'''
A program to turn a catalog file into a ds9 region file
'''

import phot_utils as pu
import Sources as S

def makeRegionFile(filename, outname):
    catalog = open(filename, "r")
    tmp = filter(lambda line: pu.noHead(line), catalog)

    sources = map(lambda line: S.SCAMSource(line), tmp)

    out = open(outname, "w")
    for source in sources:
        out.write("physical;circle(" + str(source.ximg) + "," +
                    str(source.yimg) + ",2) #color=red" + "\n")
