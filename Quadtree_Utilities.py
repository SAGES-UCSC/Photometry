'''
Help functions and classes for the Quadtree
'''

class Interest:
    def __init__(self, x, y, dist, bounds):
        self.tx = x
        self.ty = y
        self.bounds = bounds

        self.update(dist)

    def update(self, dist):
        self.xmin = self.tx - dist
        self.ymin = self.ty - dist
        self.xmax = self.tx + dist
        self.ymax = self.ty + dist

        self.xmin = max(self.xmin, self.bounds.xmin)
        self.ymin = max(self.ymin, self.bounds.ymin)
        self.xmax = min(self.xmax, self.bounds.xmax)
        self.ymax = min(self.ymax, self.bounds.ymax)


class Nearest:
    def __init__(self, dist):
        self.source = None
        self.dist2 = dist

class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]

