'''
Help functions and classes for the Quadtree
'''

class Interest:
    def __init__(self, x, y, dist, bounds):
    #def __init__(self, xmin, ymin, xmax, ymax, bounds):
        self.tx = x
        self.ty = y

        self.update(dist, bounds)

    def clip(self, bounds):
        self.xmin = max(self.xmin, bounds.xmin)
        self.ymin = max(self.ymin, bounds.ymin)
        self.xmax = min(self.xmax, bounds.xmax)
        self.ymax = min(self.ymax, bounds.ymax)

    def update(self, dist, bounds):
        self.xmin = self.tx - dist
        self.ymin = self.ty - dist
        self.xmax = self.tx + dist
        self.ymax = self.ty + dist

        self.clip(bounds)

class Nearest:
    def __init__(self, dist):
        self.source = None
        self.dist = dist

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

