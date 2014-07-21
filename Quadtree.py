import math
from bigfloat import *

import geom_utils as gu
#import _norm
import _angular_dist
import Quadtree_Utilities as utils

LEAF_MAX = 70
class Quadtree(object):
    """
    Quadtree base class. Only functions that are agnostic to
    the type of coordinate system or source object used. Must
    use a subclass.
    """
    def __init__(self, xmin, ymin, xmax, ymax):
        self.top = Node(xmin, ymin, xmax, ymax)
        self.num_subdivides = 0
        self.num_insert = 0
        self.num_inserttonodes = 0
        self.num_matched = 0
        self.num_inserttoquads = 0
        self.num_nearersources = 0
        self.verbose = False

    def inserttonode(self, node, source):
        self.num_inserttonodes+=1
        if len(node.contents) == LEAF_MAX:
            self.subdivide(node)
        if node.q1:
            self.inserttoquad(node, source)
        else:
            node.contents.append(source)

    def inserttoquad(self, node, source):
        self.num_inserttoquads+=1
        if source.x >= node.xmid:
            if source.y >= node.ymid:
                quadrant = node.q1
            else:
                quadrant = node.q4
        else:
            if source.y >= node.ymid:
                quadrant = node.q2
            else:
                quadrant = node.q3
        self.inserttonode(quadrant, source)

    def subdivide(self, node):
        self.num_subdivides+=1
        node.q1 = Node(node.xmid, node.ymid, node.xmax, node.ymax)
        node.q2 = Node(node.xmin, node.ymid, node.xmid, node.ymax)
        node.q3 = Node(node.xmin, node.ymin, node.xmid, node.ymid)
        node.q4 = Node(node.xmid, node.ymin, node.xmax, node.ymid)
        while node.contents:
            self.inserttoquad(node, node.contents.pop())

    def match(self, x, y):
        self.num_matched+=1
        dist = self.initial_dist(self.top.xmax, self.top.xmin,
                                 self.top.ymax, self.top.ymin)
        nearest = utils.Nearest(dist*dist)

        interest = utils.Interest(x, y, dist, self.top)

        self.nearersource(self.top, interest, nearest)
        return nearest.source

    def nearersource(self, node, interest, nearest):
        self.num_nearersources+=1
        if interest.intersect(node):
            if self.verbose:
                print "Intersecting Quadtrant: "
            if node.q1 == None:
                for s in node.contents:
                    dist2 = self.norm2(s.x, s.y, interest.tx, interest.ty)
                    if dist2 < nearest.dist2:
                        if self.verbose:
                            print "     Searching"
                            print "     ", dist2
                        nearest.source = s.source
                        nearest.dist2 = dist2
                        interest.update(math.sqrt(dist2))
            else:
                self.nearersource(node.q1, interest, nearest)
                self.nearersource(node.q2, interest, nearest)
                self.nearersource(node.q3, interest, nearest)
                self.nearersource(node.q4, interest, nearest)

    """
    Functions to aid in testing and debugging.
    """

    def sources_region(self, root):
        """
        Walk the tree and make a region file to check that insert is working.
        """
        with open("tree_sources.reg", "a") as region:
            if root.q1 == None:
                for s in root.contents:
                    region.write("physical;circle(" + str(s.x) + "," \
                                    + str(s.y) +  " 10) #color=blue \n")
            else:
                self.sources_region(root.q1)
                self.sources_region(root.q2)
                self.sources_region(root.q3)
                self.sources_region(root.q4)

    def leaf_region(self, root):
        """
        For visualizing the quadtree on a .fits image with ds9 region file.
        """
        with open("tree_leaves.reg", "a") as region:
            if root.q1 == None:
                region.write("physical;ruler(" + str(root.xmin) + "," + \
                                str(root.ymin) + "," + str(root.xmax) + \
                                "," + str(root.ymax) +  ") # ruler=pixels \n")

            else:
                self.leaf_region(root.q1)
                self.leaf_region(root.q2)
                self.leaf_region(root.q3)
                self.leaf_region(root.q4)

    def debug(self):
        print "Number of subdivides: %d" % self.num_subdivides
        print "Inserttonode was called %d times" % self.num_inserttonodes
        print "Matched was called %d times" % self.num_matched
        print "Inserttoquad was called %d times" % self.num_inserttoquads
        print "Nearer sources was called %d times" % self.num_nearersources
        print "Insert was called %d times" % self.num_insert

class Node(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = BigFloat(xmin)
        self.ymin = BigFloat(ymin)
        self.xmax = BigFloat(xmax)
        self.ymax = BigFloat(ymax)
        self.xmid = BigFloat((self.xmin + self.xmax)/2.0)
        self.ymid = BigFloat((self.ymin + self.ymax)/2.0)
        self.q1 = self.q2 = self.q3 = self.q4 = None
        self.contents = []

class Point(object):
    """
    The point of Point (heh.) is to have a uniform object that
    can be passed around the Quadtree. This makes for
    easy switching between equatorial and pixel coordinate
    systems or different objects.
    """
    def __init__(self, source, x, y):
        self.source = source
        self.x = BigFloat(x)
        self.y = BigFloat(y)

class ScamPixelQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamPixelQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.top, Point(source, source.ximg, source.yimg))

    def norm2(self, x1, y1, x2, y2):
#        return _norm.norm2(x1, y1, x2, y2)
        return gu.pixnorm2(x1, y1, x2, y2)

    def initial_dist(self, x2, x1, y2, y1):
        return  min((x2) - (x1), (y2) - (y1))

class ScamEquatorialQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamEquatorialQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.top, Point(source, source.ra, source.dec))

    def norm2(self, x1, y1, x2, y2):
        return _angular_dist.angular_dist2(x1, y1, x2, y2)

    def initial_dist(self, x2, x1, y2, y1):
        return  min((x2) - (x1), (y2) - (y1))

