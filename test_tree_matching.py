'''
Testing the quadtree
'''
import sys

import Sources
import Quadtree
import phot_utils
import _angular_dist
import _norm

def associate(list1, tree2):
    dist = 5
    with open("test.reg", "w") as out:
        for entry in list1:
            match2 = tree2.match(entry.ximg, entry.yimg)
            if match2 != None and _norm.norm(entry.ximg, entry.yimg, match2.ximg, match2.yimg) <= dist:
                out.write("physical;circle(" + str(entry.ximg) + "," + str(entry.yimg) +
                            " 10) #color=red \n")

with open('NGC4621_i.cat', 'r') as f:
    i_catalog = [Sources.SCAMSource(line) for line in f if phot_utils.no_head(line)]

with open('NGC4621_g.cat', 'r') as f:
    g_catalog = [Sources.SCAMSource(line) for line in f if phot_utils.no_head(line)]

ximg = [source.ximg for source in i_catalog]
yimg = [source.yimg for source in i_catalog]
sources = Quadtree.ScamPixelQuadtree(min(ximg), min(yimg), max(ximg), max(yimg))

#ra = [source.ra for source in i_catalog]
#dec = [source.dec for source in i_catalog]
#sources = Quadtree.ScamEquatorialQuadtree(min(ra), min(dec), max(ra), max(dec))

[sources.insert(source) for source in i_catalog]

#match = sources.match(190.7027198, 11.3355764)
#match = sources.match(2799.225, 3.474)

associate(g_catalog, sources)

#sources.debug()
#print match.line

