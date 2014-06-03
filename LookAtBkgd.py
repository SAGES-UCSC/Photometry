'''
Make a plot of the the background values
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import Sources as S
from numpy.random import randn

left, width = 0.12, 0.55
bottom, height = 0.12, 0.55
bottom_h = left_h = left+width+0.02

rect_noise = [left, bottom, width, height] # dimensions of temp plot

axNoise = plt.axes(rect_noise) # temperature plot

file1 = open("ap_4.31578947368noise.txt", "r")

dets = map(lambda line: S.SCAMSource(line), file1)
noise = map(lambda s: s.mag_aper, dets)
x = map(lambda s: s.ximg, dets)
y = map(lambda s: s.yimg, dets)

xmin = min(noise)
xmax = max(noise)
ymin = min(noise)
ymax = max(noise)

nxbins = 50
nybins = 50
nbins = 100

xbins = np.linspace(start = xmin, stop = xmax, num = nxbins)
ybins = np.linspace(start = ymin, stop = ymax, num = nybins)
xcenter = (xbins[0:-1]+xbins[1:])/2.0
ycenter = (ybins[0:-1]+ybins[1:])/2.0
aspectratio = 1.0*(xmax - 0)/(1.0*ymax - 0)

H, xedges,yedges = np.histogram2d(y,x,bins=(ybins,xbins))
X = xcenter
Y = ycenter
Z = H

cax = (axNoise.imshow(H, extent=[xmin,xmax,ymin,ymax],
           interpolation='nearest', origin='lower',aspect=aspectratio))
plt.show()

