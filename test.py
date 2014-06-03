import random as r
import Quadtree
import Sources as S
import phot_utils

sources = Quadtree.ScamPixelQuadtree(0, 0, 15000, 15000)

with open("/Users/alexawork/Documents/GlobularClusters/Photometry/NGC4649/NGC4649_g.cat") as f:
    tmp = filter(lambda line: phot_utils.no_head(line), f)
map(lambda line: sources.insert(S.SCAMSource(line)), tmp)

sources.match(10, 15)
sources.debug()
