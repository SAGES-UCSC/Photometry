'''
Quadtree superclass. Only functions that are agnostic to type of coordinates used.
'''
import math
import geom_utils as gu

MAX = 50

class Quadtree(object):
    class Node(object):
        def __init__(self, xmin, ymin, xmax, ymax):
            self.xmin = float(xmin)
            self.ymin = float(ymin)
            self.xmax = float(xmax)
            self.ymax = float(ymax)
            self.xmid = (self.xmin + self.xmax)/2
            self.ymid = (self.ymin + self.ymax)/2
            self.q1 = self.q2 = self.q3 = self.q4 = None
            self.contents = []

    class Point(object):
        def __init__(self, source, x, y):
            self.source = source
            self.x = float(x)
            self.y = float(y)

    def __init__(self, xmin, ymin, xmax, ymax, **kwargs):
        if 'coord' in kwargs:
            self.coord = kwargs['coord']
        else:
            self.coord = None
        if 'objtype' in kwargs:
            self.objtype = kwargs['objtype']
        else:
            self.objtype = None
        self.top = Node(xmin, ymin, xmax, ymax)
        self.num_subdivides = 0
        self.num_insert = 0
        self.num_inserttonodes = 0
        self.num_matched = 0
        self.num_inserttoquads = 0
        self.num_nearersources = 0

    def debug(self):
        print "Number of subdivides: ", self.num_subdivides
        print "Inserttonode was called %d times", self.num_inserttonodes
        print "Matched was called %d times", self.num_matched
        print "Inserttoquad was called %d times", self.num_inserttoquads
        print "Nearer sources was called %d times", self.num_nearersources
        print "Insert was called %d times", self.num_insert

    def insert(self, source):
        self.num_insert+=1
        # Any way to move this into __init__(). It's unnecessary to
        # To do this for every
        if self.objtype == 'subaru' or self.objtype == None:
            if self.coord == 'pixel' or self.coord == None:
                source = scamPixel(source)
            elif self.coord == 'equatorial':
                source = scamEquatorial(source)
        elif self.objtype == 'vizier':
            source = vizerEquatorial(source)

        self.inserttonode(self.top, source)

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
        # pop the list and insert the sources as they come off
        while node.contents:
            self.inserttoquad(node, node.contents.pop())

    def match(self, x, y):
        self.num_matched+=1
        return self.nearestsource(self, x, y)

    def nearestsource(self, tree, x, y):
        nearest = {'source':None, 'dist':0}
        # Need to include this next line somehow in the subclasses
        nearest['dist'] = min(tree.top.xmax - tree.top.xmin,
                              tree.top.ymax - tree.top.ymin)/1000.0
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
                    if self.coord == 'pixel' or self.coord == None:
                        s_dist = gu.pixnorm2(s.x, s.y, x, y)
                    elif self.coord == 'equatorial':
                        s_dist = gu.equnorm2(s.x, s.y, x, y)
                    if s_dist < nearest['dist']:
                        nearest['source'] = s
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

class ScamPixelQuadtree(Quadtree):
    def __init__(self, xmin, ymin, xmax, ymax):
        super(ScamPixelQuadtree, self).__init__(xmin, ymin, xmax, ymax)
    def insert(self, source):
        self.num_insert+=1
        self.inserttnode(self.top, Point(source, source.ximg, source.yimg))

class ScamEquatorialQuadtree(Quadtree):
    def __init__(self, node):
        super(scamEquatorial, self).__init__(xmin, ymin, xmax, ymax)
    def insert(self, source):
        self.num_insert+=1
        self.inserttnode(self.top, Point(source, source.ra, source.dec))

class VizierEquatorialQuadtree(Quadtree):
    def __init__(self, node):
        super(vizierEquatorial, self).__init__(node.xmin, node.ymin, node.xmax, node.ymax)
    def insert(self, source):
        self.num_insert+=1
        self.inserttnode(self.top, Point(source, source['RAJ2000'], source['DEJ2000']))

