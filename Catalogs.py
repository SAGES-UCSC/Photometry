"""
A class to keep track of the methods for catalog files
"""

class ScamCatalog(object):
    def __init__(self, fname):
        self.data = open(fname, 'r')
        line_count = 0
        # Need to change this just to skip any line starting with '#'
        while True:
            if line_count < 27:
                self.data.readline()
            else:
                line = self.data.readline()
                line = line.lstrip()
                if line[0] == '#':
                    break
            line_count+=1

        self.header = ["number", "flux_iso", "fluxerr_iso", "flux_aper", \
                "fluxerr_aper", "ximg", "yimg", "ra", "dec", "mag_auto", "magerr_auto", \
                "mag_best", "magerr_best", "mag_aper", "magerr_aper", "a_world", \
                "a_world_err", "b_world", "b_world_err", "theta_err", "theta", "isoarea", \
                "mu_max", "flux_radius", "flags", "fwhm", "elongation", "vignet"]

    def next(self):
        line = self.data.readline()
        line = line.lstrip()
        if line == "":
            self.data.close()
            raise StopIteration()

        cols = line.split()
        if len(cols) != len(self.header):
            print "Input catalog is not valid."
            raise StopIteration()

        for element, col in zip(self.header, cols):
            self.__dict__.update({element:float(col)})
        self.__dict__.update({"match2":None})
        self.__dict__.update({"match3":None})

        return self.__dict__.copy()

    def __iter__(self):
        return self

    # Need to figure out how to write out a catalog when match2 and
    # mach3 != None
    def catalog_write(self, outname):
        with open(outname, "w") as out:
            out.write("    ".join(self.header) + "\n")
            for source in self:
                out.write("    ".join(map(str, source)) + "\n")


