'''
Implement a quadtree
'''

class Quadtree():
    def __init__(xmin, ymin, xmax, ymax):
        self.xmin  = xmin
        self.ymin  = ymin
        self.xmax  = xmax
        self.ymax  = ymax

    def newnode(xmin, ymin, xmax, ymax):
        self.name = blah.blah
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.xmix = (xmin + xmax)/2
        self.ymix = (ymin + ymax)/2
        self.q1 = self.q2 = self.q3 = self.q4 = NONE
        self.contents = WHAT

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
            # If no subquads exist add source to the list in contents element

    def subdivide(node):
        node.q1 = new_node()
        node.q2 = new_node()
        node.q3 = new_node()
        node.q4 = new_node()

        # pop the list and insert the sources as they come off

    def nearestsource(tree, x, y):
        # Initalize a box of interest
        dist = SOMETHING
        interest.xmin = x - dist
        interest.ymin = x - dist
        interest.xmax = x + dist
        interest.ymax = x + dist

        # How to keep track of nearest now?
        nearer_source(tree, tree, x, y, interest, nearest,  dist)

    def nearersource(tree, node, x, y, interest, nearest, dist):

# What do I need to give this?
class Box():
    def __init__():
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

class Node():
    def __init__():
        self.box = Box() # How to do this actually?
        self.xmid = xmid
        self.ymid = ymid
        self.q1 = Node()
        self.q2 = Node()
        self.q3 = Node()
        self.q4 = Node()
        self.contents = S.SCAMSources()
