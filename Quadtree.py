'''
Implement a quadtree
'''
import geom_utils as gu
import math

MAX = 12

class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.top = Node(xmin, ymin, xmax, ymax)

    def insert(self, source):
        self.inserttonode(self.top, source)

    def inserttonode(self, node, source):
        if len(node.contents) == MAX:
            self.subdivide(node)

        if node.q1:
            self.inserttoquad(node, source)
        else:
            # If no subquads exist add source to the list in CONTENTS element
            node.contents.append(source)

    def inserttoquad(self, node, source):
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
        self.inserttonode(quadrant, source)

    def subdivide(self, node):
        node.q1 = Node(node.xmid, node.ymid, node.xmax, node.ymax)
        node.q2 = Node(node.xmin, node.ymid, node.xmid, node.ymax)
        node.q3 = Node(node.xmin, node.ymin, node.xmid, node.ymid)
        node.q4 = Node(node.xmid, node.ymin, node.xmax, node.ymid)

        # pop the list and insert the sources as they come off
        while node.contents:
            self.inserttoquad(node, node.contents.pop())

    def match(self, x, y):
        self.nearestsource(self, x, y)

    def nearestsource(self, tree, x, y):
        nearest = None

        # Initalize a box of interest
        dist = gu.dblmin(tree.top.xmax - tree.top.xmin, tree.top.ymax - tree.top.ymin)
        interest = {'xmin':x-dist, 'ymin':y-dist, 'xmax':x+dist, 'ymax':y+dist,}
        interest = gu.clip_box(interest['xmin'], interest['xmax'], interest['ymin'], interest['ymax'],
                    tree.top.xmin, tree.top.xmax, tree.top.ymin, tree.top.ymax)
        dist = dist * dist

        nearest = self.nearersource(tree, tree.top, x, y, interest, nearest,  dist)
        print nearest
        return nearest

    def nearersource(self, tree, node, x, y, interest, nearest, dist):
        if gu.intersecting(node.xmin, node.xmax, node.ymin, node.ymax,
                            interest['xmin'], interest['xmax'], interest['ymin'], interest['ymax']):
            if node.q1 == None:
                for s in node.contents:
                    s_dist = gu.norm(s.ximg, s.yimg, x, y)
                    if (s_dist < dist):
                        nearest = s
                        dist = s_dist
                        s_dist = math.sqrt(s_dist)
                        interest['xmin'] = x - s_dist
                        interest['ymin'] = y - s_dist
                        interest['xmax'] = x + s_dist
                        interest['ymax'] = y + s_dist
                        interest = gu.clip_box(interest['xmin'], interest['xmax'], interest['ymin'], interest['ymax'],
                                    tree.top.xmin, tree.top.xmax, tree.top.ymin, tree.top.ymax)
            else:
                self.nearersource(tree, node.q1, x, y, interest, nearest, dist)
                self.nearersource(tree, node.q2, x, y, interest, nearest, dist)
                self.nearersource(tree, node.q3, x, y, interest, nearest, dist)
                self.nearersource(tree, node.q4, x, y, interest, nearest, dist)

        return nearest

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
