import random as r
import Quadtree
import Sources as S
import phot_utils
'''
class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax, **kwargs):
        if 'coord' in kwargs:
            self.coord = kwargs['coord']
        else:
            self.coord = None
        self.node = Node(xmin, ymin, xmax, ymax)
        if self.coord == 'pixel' or self.coord == None:
            self.blah = Pixel(self.node)
        else:
            self.blah = Equatorial(self.node)
        print self.blah

    def insert(self):
        if self.coord == 'pixel' or self.coord == None:
            x = Pixel(self.node)
            x.blargh(self.node)
        elif self.coord == 'equatorial':
            Equatorial(self.node)
            x = Equatorial(self.node)
            x.blargh(self.node)

    def match(self):
        if self.coord == 'pixel' or self.coord == None:
            x = Pixel(self.node)
            x.match(self.node)
        elif self.coord == 'equatorial':
            x = Equatorial(self.node)
            x.match(self.node)

class Pixel(Quadtree):
    def __init__(self, node):
        print 'Pixel!'
    def blargh(self, node):
        print geom_utils.pixnorm(node.xmin, node.ymin, node.xmax, node.ymax)
    def match(self, node):
        print "Pixel matching!"

class Equatorial(Quadtree):
    def __init__(self, node):
        print 'Equatorial!'
    def blargh(self, node):
        print geom_utils.equnorm(node.xmin, node.ymin, node.xmax, node.ymax)
    def match(self, node):
        print "radec matching!"

class Node:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)

x = Quadtree(1, 2, 3, 4, coord = 'pixel')
y = Quadtree(1, 2, 3, 4, coord = 'equatorial')
z = Quadtree(1, 2, 3, 4)

#x.insert()
#y.insert()
#z.insert()

#x.match()
#y.match()
#z.match()
'''

sources = Quadtree.Quadtree(0, 0, 15000, 15000, coord='pixel')

with open("/Users/alexawork/Documents/GlobularClusters/Photometry/NGC4649/NGC4649_g.cat") as f:
    tmp = filter(lambda line: phot_utils.no_head(line), f)
map(lambda line: sources.insert(S.SCAMSource(line)), tmp)

sources.match(10, 15)
sources.debug()
