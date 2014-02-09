'''
Implement a quadtree
'''

class Quadtree():
    def __init__(xmin, ymin, xmax, ymax):
        self.xmin  = xmin
        self.ymin  = ymin
        self.xmax  = xmax
        self.ymax  = ymax

    def __newnode__(xmin, ymin, xmax, ymax):
        self.name = blah.blah
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmix = (xmin + xmax)/2
        self.ymix = (ymin + ymax)/2
        self.q1 = self.q2 = self.q3 = self.q4 = NONE

    # I don't want to schlep all the contents around
    # Just want to return an identifier so I can get
    # the matched items afterward
    def __newsource__():

    def __insertsource__(node, source):
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
            # If no subquads exist add source to the list in contents element

    def __subdivide__(node):
        node.q1 = new_node()
        node.q2 = new_node()
        node.q3 = new_node()
        node.q4 = new_node()

        # pop the list and insert the sources as they coe off

    def __nearestsource__(tree, x, y):
        # Initalize a box of interest
        dist = SOMETHING
        interest.xmin = x - dist
        interest.ymin = x - dist
        interest.xmax = x + dist
        interest.ymax = x + dist

        # How to keep track of nearest now?
        nearer_source(tree, tree, x, y, interest, nearest,  dist)

    def __nearersource__(tree, node, x, y, interest, nearest, dist):


class Source():

class Node():
