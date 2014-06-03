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
        elf.b_world = float(cols[12])

class SCAMSource:
    def __init__(self, line):
        self.line = line
        cols = line.split()
        self.name = cols[0]
        self.flux_iso = float(cols[1])
        self.fluxerr_iso = float(cols[2])
        self.flux_aper = float(cols[3])
        self.fluxerr_aper = float(cols[4])
        self.ximg = float(cols[5])
        self.yimg = float(cols[6])
        self.ra = float(cols[7])
        self.dec = float(cols[8])
        self.mag_auto = float(cols[9])
        self.mag_auto_err = float(cols[10])
        self.mag_best = float(cols[11])
        self.mag_best_err = float(cols[12])
        self.mag_aper = float(cols[13])
        self.mag_aper_err = float(cols[14])
        self.a_world = float(cols[15])
        self.a_world_err = float(cols[16])
        self.b_world = float(cols[17])
        self.b_world_err = float(cols[18])
        self.theta_err = float(cols[19])
        self.theta  = float(cols[20])
        self.isoarea  = float(cols[21])
        self.mu  = float(cols[22])
        self.flux_radius = float(cols[23])
        self.flags = float(cols[24])
        self.fwhm = float(cols[26])
        self.elogation = float(cols[27])
        self.vignet = float(cols[28])
        self.match2 = None
        self.match3 = None

class TESTSource:
    def __init__(self, line):
        self.line = line
        cols = line.split()
        self.ximg = float(cols[0])
        self.yimg = float(cols[1])

#class ACSSource:
#    def _init_(self, line):
#        self.line = line
#        cols = line.split()
#        self.name = cols[0]
#        self.ra = cols[]
#        self.dec = cols[]
#        self.size1 = cols[]
#        self.size2 = cols[]
#        self.size3 = cols[]
#        self.mag1 = cols[]
#        self.mag2 = cols[]
#        self.mag3 = cols[]



#class ACSSource:
#    def _init_(self, line):
#        self.line = line
#        cols = line.split()
#        self.name = cols[0]
#        self.ra = cols[]
#        self.dec = cols[]
#        self.size1 = cols[]
#        self.size2 = cols[]
#        self.size3 = cols[]
#        self.mag1 = cols[]
#        self.mag2 = cols[]
#        self.mag3 = cols[]


