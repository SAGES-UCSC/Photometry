'''
Implement a quadtree
'''
import geom_utils as gu

class Quadtree:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.top = Node(xmin, ymin, xmax, ymax)

    def insertsource(node, source):
        if node.contents.length == MAX:
            subdivide(node)

        if node.q1 != None:
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

            insertsource(quadrant, source)

        else:
            # If no subquads exist add source to the list in CONTENTS element
            node.contents.append(source)

    def inserttoquad(node, source)
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

    def subdivide(node):
        node.q1 = Node(node.xmid, node.ymid, node.xmax, node.ymax)
        node.q2 = Node(node.xmin, node.ymid, node.xmid, node.ymax)
        node.q3 = Node(node.xmin, node.ymin, node.xmid, node.ymid)
        node.q4 = Node(node.xmid, node.ymin, node.xmax, node.ymid)

        # pop the list and insert the sources as they come off
        while node.contents:
            inserttoquad(node, node.contents.pop())

    def nearestsource(tree, x, y):
        # Initalize a box of interest
        dist = gu.dblmin(tree.xmax - tree.xmin, tree.ymax - tree.ymin)
        interest.xmin = x - dist
        interest.ymin = x - dist
        interest.xmax = x + dist
        interest.ymax = x + dist
        gu.clip_box(interest, xmin, ymin, xmax, ymax)
        dist = dist * dist

        # How to keep track of nearest now?
        nearer_source(tree, tree, x, y, interest, nearest,  dist)

    def nearersource(tree, node, x, y, interest, nearest, dist):
        if gu.interestecting(node, interest):
            if node.q1 == None:
                for s in node.contents():
                    s_dist = norm(s.ximg, s.yimg, x, y)
                    if (s_dist < dist):
                        nearest = s
                        dist = s_dist

                        s_dist = sqrt(s_dist)
                        interest.xmin = x - s_dist
                        interest.ymin = y - s_dist
                        interest.xmax = x + s_dist
                        interest.ymax = y + s_dist
                        gu.clip_box(interest, tree)
            else:
                nearer_source(tree, node.q1, x, y, interest, nearest, dist)
                nearer_source(tree, node.q2, x, y, interest, nearest, dist)
                nearer_source(tree, node.q3, x, y, interest, nearest, dist)
                nearer_source(tree, node.q4, x, y, interest, nearest, dist)

class Node:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmid = (xmin + xmax)/2
        self.ymid = (ymin + ymax)/2
        self.contents = []

