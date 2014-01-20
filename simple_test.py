'''
AUTHOR:
    Alexa Villaume, UCSC

PURPOSE:
    A program demonstrating how to use the geom_utils and phot_utils packages.

INPUT PARAMETERS:
    A photometry source catalog
    The equation of a line for the color cut

OUTPUT:
    A catalog of of GC candidates

NOTES:

'''

import numpy as np
import phot_utils as pu
import geom_utils as gu
import Sources as S

# For color selection
# Have the slope, y-intercept, and endpoints from M87 data
# This is for <u-z> vs <g-z> space.
b = -0.086
m = 0.50
x0 = 1.5
x1 = 3.0
var = 0.3   # This controls how strict the color cut is

catalog = open("n4459_cfht_ugiz_auto.cat", "r")
catalog.next() # This is to skip the header

# This reads in the catalog and initalizes each line as a
# CFHT source
sources = map(lambda line: S.CFHTSource(line), catalog)

# Make the color cut
candidates = filter(lambda s: pu.makeColorCut(s.mag1, s.mag4, s.mag2, s.mag4, x0, x1, m, b, var), sources)

# Finds the value of a_world that seems to "contain" the point-like sources
shape = map(lambda s: s.a_world, candidates)
peak = pu.detHistPeak(shape, 1000)
print "Estimated peak: ", peak

# Make shape cut based on value found in previous step
candidates = filter(lambda s: s.a_world <= peak, candidates)

output = open("GC_Candidates.txt", "w")
for source in candidates:
    output.write(source.line)

