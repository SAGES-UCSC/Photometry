import math
#from bigfloat import *

import geom_utils as gu
import _norm
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
        self.root = Node(xmin, ymin, xmax, ymax)
        self.num_insert = 0
        self.num_inserttonodes = 0
        self.num_inserttoquads = 0
        self.num_subdivides = 0
        self.num_matched = 0
        self.num_tree_climb_boxs = 0
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

    def match(self, tx, ty):
        self.num_matched+=1
        dist = self.initial_dist(self.root.xmax, self.root.xmin,
                                 self.root.ymax, self.root.ymin)
        nearest = utils.Nearest(dist*dist)
        interest = utils.Interest(tx, ty, dist, self.root)

        self.tree_climb_point(self.root, interest, nearest)
        self.tree_climb_box(self.root, interest, nearest)
        return nearest.source

    def leaf_walk(self, node, interest, nearest):
        old_dist2 = nearest.dist2
        for s in node.contents:
            dist2 = self.norm2(s.x, s.y, interest.tx, interest.ty)
            if dist2 < nearest.dist2:
                nearest.source = s.source
                nearest.dist2 = dist2
        if nearest.dist2 < old_dist2:
            interest.update(math.sqrt(nearest.dist2))

    def tree_climb_point(self, node, interest,  nearest)
        self.num_tree_climb_boxs+=1
        if gu.in_box(node.xmin, node.xmax, node.ymin,
                    node.ymax, interest.tx, interest.ty)
            if node.q1 == None:
                self.leaf_walk(node, interest, nearest)
            else:
                self.tree_climb_point(node.q1, interest, nearest)
                self.tree_climb_point(node.q2, interest, nearest)
                self.tree_climb_point(node.q3, interest, nearest)
                self.tree_climb_point(node.q4, interest, nearest)

    def tree_climb_box(self, node, interest, nearest):
        self.num_tree_climb_boxs+=1
        if interest.intersect(node):
            if node.q1 == None:
                self.leaf_walk(node, interest, nearest)
            else:
                self.tree_climb_box(node.q1, interest, nearest)
                self.tree_climb_box(node.q2, interest, nearest)
                self.tree_climb_box(node.q3, interest, nearest)
                self.tree_climb_box(node.q4, interest, nearest)

    """
    Functions to aid in testing and debugging.
    """

    #def get_depth(self, node):
        #"""
        #Create histogram of depths.
        #"""

    def sources_region(self, node):
        """
        Pass the function the root of the tree. Walk the tree
        and make a region file to check that insert is working.
        """
        with open("tree_sources.reg", "w") as region:
            if node.q1 == None:
                for s in node.contents:
                    region.write("physical;circle(" + str(s.x) + "," \
                                    + str(s.y) +  " 10) #color=blue \n")
            else:
                self.sources_region(node.q1)
                self.sources_region(node.q2)
                self.sources_region(node.q3)
                self.sources_region(node.q4)

    def leaf_region(self, node):
        """
        Pass the function the root of the tree. For visualizing
        the quadtree on a .fits image with ds9 region file.
        """
        with open("tree_leaves.reg", "w") as region:
            if node.q1 == None:
                region.write("physical;ruler(" + str(node.xmin) + "," + \
                                str(node.ymin) + "," + str(node.xmax) + \
                                "," + str(node.ymax) +  ") # ruler=pixels \n")

            else:
                self.leaf_region(node.q1)
                self.leaf_region(node.q2)
                self.leaf_region(node.q3)
                self.leaf_region(node.q4)

    def debug(self):
        print "\n"
        print "Insert was called %d times" % self.num_insert
        print "Inserttonode was called %d times" % self.num_inserttonodes
        print "Inserttoquad was called %d times" % self.num_inserttoquads
        print "Number of subdivides: %d" % self.num_subdivides
        print "Matched was called %d times" % self.num_matched
        print "Nearer sources was called %d times" % self.num_tree_climb_boxs
        print "\n"

class Node(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmid = (self.xmin + self.xmax)/2.0
        self.ymid = (self.ymin + self.ymax)/2.0
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
        self.x = x
        self.y = y

class ScamPixelQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamPixelQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.root, Point(source, source.ximg, source.yimg))

    def norm2(self, x1, y1, x2, y2):
        return _norm.norm2(x1, y1, x2, y2)

    def initial_dist(self, x2, x1, y2, y1):
        return  min(x2 - x1, y2 - y1)

class ScamEquatorialQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamEquatorialQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.root, Point(source, source.ra, source.dec))

    def norm2(self, x1, y1, x2, y2):
        return _angular_dist.angular_dist2(x1, y1, x2, y2)

    def initial_dist(self, x2, x1, y2, y1):
        return  min(x2 - x1, y2 - y1)
