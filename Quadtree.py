from __future__ import division
import math
import geom_utils as gu

MAX = 50

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

    def debug(self):
        print "Number of subdivides: %d" % self.num_subdivides
        print "Inserttonode was called %d times" % self.num_inserttonodes
        print "Matched was called %d times" % self.num_matched
        print "Inserttoquad was called %d times" % self.num_inserttoquads
        print "Nearer sources was called %d times" % self.num_nearersources
        print "Insert was called %d times" % self.num_insert

    def inserttonode(self, node, source):
        self.num_inserttonodes+=1
        if len(node.contents) == MAX:
            self.subdivide(node)
        if node.q1:
            self.inserttoquad(node, source)
        else:
            # If no subquads exist add source to the list in CONTENTS element
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
        # Pop the list and insert the sources as they come off
        print node.xmin, node.xmax, node.ymin, node.ymax
        while node.contents:
            self.inserttoquad(node, node.contents.pop())

    def match(self, x, y):
        self.num_matched+=1
        return self.nearestsource(self, x, y)

    def nearestsource(self, tree, x, y):
        nearest = {'source':None, 'dist':0}
        nearest['dist'] = self.initial_dist(tree.top.xmax, tree.top.xmin,
                                       tree.top.ymax, tree.top.ymin)
        interest = {'xmin':x-nearest['dist'], 'ymin':y-nearest['dist'],
                    'xmax':x+nearest['dist'], 'ymax':y+nearest['dist']}
        interest = gu.clip_box(interest['xmin'], interest['ymin'],
                               interest['xmax'], interest['ymax'],
                               tree.top.xmin, tree.top.ymin,
                               tree.top.xmax, tree.top.ymax)
        nearest['dist'] = nearest['dist']*nearest['dist']

        self.nearersource(tree, tree.top, x, y, nearest, interest)
        return nearest['source']

    def nearersource(self, tree, node, x, y, nearest, interest):
        self.num_nearersources+=1
        if gu.intersecting(node.xmin, node.xmax, node.ymin, node.ymax,
                          interest['xmin'], interest['xmax'],
                          interest['ymin'], interest['ymax']):
            if node.q1 == None:
                for s in node.contents:
                    s_dist = self.norm2(s.x, s.y, x, y)
                    if s_dist < nearest['dist']:
                        nearest['source'] = s.source
                        nearest['dist'] = s_dist
                        dist = math.sqrt(s_dist)
                        interest['xmin'] = x - dist
                        interest['ymin'] = y - dist
                        interest['xmax'] = x + dist
                        interest['ymax'] = y + dist
                        interest = gu.clip_box(interest['xmin'], interest['ymin'],
                                           interest['xmax'], interest['ymax'],
                                           tree.top.xmin, tree.top.ymin,
                                           tree.top.xmax, tree.top.ymax)
            else:
                self.nearersource(tree, node.q1, x, y, nearest, interest)
                self.nearersource(tree, node.q2, x, y, nearest, interest)
                self.nearersource(tree, node.q3, x, y, nearest, interest)
                self.nearersource(tree, node.q4, x, y, nearest, interest)

class Node(object):
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)
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
        self.x = float(x)
        self.y = float(y)

class ScamPixelQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamPixelQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.top, Point(source, source.ximg, source.yimg))

    def norm2(x1, y1, x2, y2):
        return gu.pixnorm2(x1, y1, x2, y2)

    def initial_dist(x2, x1, y2, y1):
        return  min(x2 - x1, y2 - y1)/1000.0

class ScamEquatorialQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamEquatorialQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.top, Point(source, source.ra, source.dec))

    def norm2(self, x1, y1, x2, y2):
        return gu.equnorm2(x1, y1, x2, y2)

    def initial_dist(self, x2, x1, y2, y1):
        return  min(x2 - x1, y2 - y1)/0.000001

class VizierEquatorialQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(VizierEquatorialQuadtree, self).__init__(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.num_insert+=1
        self.inserttonode(self.top, Point(source, source['RAJ2000'], source['DEJ2000']))

    def norm2(x1, y1, x2, y2):
        return gu.equnorm2(x1, y1, x2, y2)

    def initial_dist(x2, x1, y2, y1):
        return  min(x2 - x1, y2 - y1)/0.1

