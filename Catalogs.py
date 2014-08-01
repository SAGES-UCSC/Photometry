"""
A class to keep track of the methods for catalog files
"""

class ScamCatalog(object):
    def __init__(self, fname):
        self.fname = fname
        self.data = object()
        self.data = lambda: None
        self.data.closed = True
        self.header = ["number", "flux_iso", "fluxerr_iso", "flux_aper", \
                "fluxerr_aper", "ximg", "yimg", "ra", "dec", "mag_auto", "magerr_auto", \
                "mag_best", "magerr_best", "mag_aper", "magerr_aper", "a_world", \
                "a_world_err", "b_world", "b_world_err", "theta_err", "theta", "isoarea", \
                "mu_max", "flux_radius", "flags", "fwhm", "elongation", "vignet"]

    def next(self):
        if self.data.closed:
            self.data = open(self.fname, "r")

        line = self.data.readline()
        line = line.lstrip()

        if line == "":
            if not self.data.closed:
                self.data.close()
            raise StopIteration()

        if line[0] == "#":
            self.next()
        else:
            cols = line.split()
            if len(cols) != len(self.header):
                print "Input catalog is not valid."
                if not self.data.closed:
                    self.data.close()
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
            out.write("# " + "    ".join(self.header) + "\n")
            for source in self:
                out.write("    ".join(map(str, [source[self.header[i]]
                            for i in range(len(self.header)) ])) + "\n")
