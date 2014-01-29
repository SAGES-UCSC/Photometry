'''
AUTHOR:
    Alexa Villaume, UCSC

PURPOSE:
    This is a collection of classes in order to make working with
    different photometry catalogs easier.
'''

class CFHTSource:
    # Take source line, split(), float them,
    def __init__(self, line):
        self.line = line
        cols = line.split()
        self.name = cols[0]
        self.ra = float(cols[1])
        self.dec = float(cols[2])
        self.mag1 = float(cols[3])
        self.mag2 = float(cols[5])
        self.mag3 = float(cols[7])
        self.mag4 = float(cols[9])
        self.mag1_err = float(cols[4])
        self.mag2_err = float(cols[6])
        self.mag3_err = float(cols[8])
        self.mag4_err = float(cols[10])
        self.a_world = float(cols[11])
        self.b_world = float(cols[12])

'''
class ACSSource:
    def _init_(self, line):
        self.line = line
        cols = line.split()
        self.name = cols[0]
        self.ra = cols[]
        self.dec = cols[]
        self.size1 = cols[]
        self.size2 = cols[]
        self.size3 = cols[]
        self.mag1 = cols[]
        self.mag2 = cols[]
        self.mag3 = cols[]
'''
