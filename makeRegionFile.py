'''
A program to turn a SCAMSources into a ds9 region files.
'''

import phot_utils
import Sources

def fromFile(filename, outname, pixsize, color):
    with open(filename, "r") as catalog:
        sources = [Sources.SCAMSource(line) for line in catalog if phot_utils.no_head(line)]
        with open(outname, "w") as out:
            for source in sources:
                out.write("physical;circle(" + str(source.ximg) + "," +
                            str(source.yimg) + "," + str(pixsize) + ") #color=" + str(color) + "\n")

def fromList(list, outname, pixsize, color):
    with open(outname, "w") as out:
        for source in list:
            out.write("j2000; circle " + str(phot_utils.convertRA(source.ra)) + "," +
                        str(phot_utils.convertDEC(source.dec)) + " .1' #color=red \n")
