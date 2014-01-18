'''
Test the geom and phot utilities. Checking that it can successfully make a catalog of
GC candidates.
'''

import phot_utils as pu
import geom_utils as gu

# For color selection
# Have the slope, y-intercept, and endpoints from M87 data
# This is for <u-z> vs <g-z> space.
b = -0.086
m = 0.50
x0 = 1.5
x1 = 3.0
var = 0.3   # This controls how strict the color cut is

catalog = open("n4459_cfht_ugiz_auto.cat", "r")
candidates = []
for source in catalog:
    cols = source.split()
    # Assuming you have four colors available to you. If you don't just put in a dummy
    # number in the appropriate element
    if cols[0][0] != '#':
        if pu.makeColorCut(float(cols[3]), float(cols[5]), float(cols[9]), -1, x0, x1, m, b, var):
            candidates.append(source)


peak = pu.detHistPeak(shape, 1000)
print "Estimated peak: ", peak

final_list = []
for source in candidates:
    if source[11] <= peak:
        final_list.append(source)

#output = open("GC_Candidates.txt", "w")
#for source in final_list:
#    output.write(source + "\n")
