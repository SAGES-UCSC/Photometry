'''
Implement a quadtree
'''

class Quadtree:
    def __init__(xmin, ymin, xmax, ymax):
        newnode(xmin, ymin, xmax, ymax)

    def newnode(xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmix = (xmin + xmax)/2
        self.ymix = (ymin + ymax)/2
        self.q1 = self.q2 = self.q3 = self.q4 = NONE
        self.contents = WHAT    # CONTENTS

    def insertsource(node, source):
        if node.contents.length == MAX:
            subdivide(node)

        if node.q1 != NONE:
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
            else:
                insertsource(quadrant, source)
        else:
        # If no subquads exist add source to the list in CONTENTS element
            node.contents.append(source)


    def subdivide(node):
        node.q1 = new_node(node.xmid, node.ymid, node.box.xmax, node.box.ymax)
        node.q2 = new_node(node.box.xmin, node.ymid, node.xmid, node.box.ymax)
        node.q3 = new_node(node.box.xmin, node.box.ymin, node.xmid, node.ymid)
        node.q4 = new_node(node.xmid, node.box.ymin, node.box.xmax, node.ymid)

        # pop the list and insert the sources as they come off
        while source = pop(node.contents):
            insertsource(node, source)

    def nearestsource(tree, x, y):
        # Initalize a box of interest
        dist = gu.dblmin(tree.box.xmax - tree.box.xmin, tree.box.ymax - tree.box.ymin)
        interest.xmin = x - dist
        interest.ymin = x - dist
        interest.xmax = x + dist
        interest.ymax = x + dist
        gu.clip_box(interest, tree.box)
        dist = dist * dist

        # How to keep track of nearest now?
        nearer_source(tree, tree, x, y, interest, nearest,  dist)

    def nearersource(tree, node, x, y, interest, nearest, dist):
        if gu.interestecting(node.box, interest):
            if node.q1 == NONE:
                for the sources in the contents list:
                    s_dist = norm(s.ximg, s.yimg, x, y)
                    if (s_dist < dist):
                        nearest = s
                        dist = s_dist

                        s_dist = sqrt(s_dist)
                        interest.xmin = x - s_dist
                        interest.ymin = y - s_dist
                        interest.xmax = x + s_dist
                        interest.ymax = y + s_dist
                        gu.clip_box(interest, tree.box)
            else:
                nearer_source(tree, node.q1, x, y, interest, nearest, dist)
                nearer_source(tree, node.q2, x, y, interest, nearest, dist)
                nearer_source(tree, node.q3, x, y, interest, nearest, dist)
                nearer_source(tree, node.q4, x, y, interest, nearest, dist)


class Box:
    def __init__(self):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

class Node:
    def __init__(self):
        self.box = Box() # How to do this actually?
        self.xmid = xmid
        self.ymid = ymid
        self.q1 = Node()
        self.q2 = Node()
        self.q3 = Node()
        self.q4 = Node()
        self.contents = # I don't know how to do this


