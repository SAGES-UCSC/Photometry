'''
Implement a quadtree
'''
import geom_utils as gu
import math

MAX = 50

class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax, **kwargs):
        self.top = Node(xmin, ymin, xmax, ymax)
        self.coord = kwargs['coord']
        self.num_subdivides = 0
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

    def insert(self, source):
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
        # Get working the res to make more flexible
        if self.coord == 'pix' or self.coord == None:
            if source.ximg >= node.xmid:
                if source.yimg >= node.ymid:
                    quadrant = node.q1
                else:
                    quadrant = node.q4
            else:
                if source.yimg >= node.ymid:
                    quadrant = node.q2
                else:
                    quadrant = node.q3
        # make sure xmid and ymid are consistent
        # fix so not hardcoding/can use different
        # object types
        elif self.coord == 'equatorial':
            if source['RAJ2000'] >= node.xmid:
                if source['DEJ2000'] >= node.ymid:
                    quadrant = node.q1
                else:
                    quadrant = node.q4
            else:
                if source['DEJ2000'] >= node.ymid:
                    quadrant = node.q1
                else:
                    quadrant = node.q4
        else:
            print "you did not enter a coordinate system recognized. Try again."
            # bail out of the proram better
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

        # Initialize a box of interest
        if self.coord == 'pix' or self.coord == None:
            nearest['dist'] = min(tree.top.xmax - tree.top.xmin,
                                  tree.top.ymax - tree.top.ymin) / 1000.0
        elif self.coord == 'equatorial':
            nearest['dist'] = min(tree.top.xmax - tree.top.xmin,
                                  tree.top.ymax - tree.top.ymin) / 1.0 # What should this be?
        else:
            print "you did not specify a coordinate system recognized"
        interest = {'xmin':x-nearest['dist'], 'ymin':y-nearest['dist'],
                    'xmax':x+nearest['dist'], 'ymax':y+nearest['dist']}
        interest = gu.clip_box(interest['xmin'], interest['ymin'], interest['xmax'], interest['ymax'],
                    tree.top.xmin, tree.top.ymin, tree.top.xmax, tree.top.ymax)
        nearest['dist'] = nearest['dist'] * nearest['dist']

        self.nearersource(tree, tree.top, x, y, nearest, interest)

        return nearest['source']

    def nearersource(self, tree, node, x, y, nearest, interest):
        self.num_nearersources+=1
        if gu.intersecting(node.xmin, node.xmax, node.ymin, node.ymax,
                            interest['xmin'], interest['xmax'], interest['ymin'], interest['ymax']):
            if node.q1 == None:
                for s in node.contents:
                    if self.coord == 'pix' or self.coord == None:
                        s_dist = gu.pixnorm2(s.ximg, s.yimg, x, y)
                    elif self.coord == 'equatorial':
                        s_dist = gu.equnorm2(s['RAJ2000'], s['DEJ2000'], x, y)
                    else:
                        print "you did not specify a coordinate system recognized"
                        # Bail out better
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

class Node:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = float(xmin)
        self.ymin = float(ymin)
        self.xmax = float(xmax)
        self.ymax = float(ymax)
        self.xmid = (self.xmin + self.xmax)/2
        self.ymid = (self.ymin + self.ymax)/2
        self.q1 = self.q2 = self.q3 = self.q4 = None
        self.contents = []
