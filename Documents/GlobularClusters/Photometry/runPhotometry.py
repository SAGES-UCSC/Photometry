#==============================================================================================#
#	Author: Alexa Villaume	
#	Date: July 30th, 2013; August 5th, 2012
#	Description: Photometry pipeline for SAGES.
#				 Refactoring code. 
#==============================================================================================#

import numpy as np
import matplotlib.pyplot as plt
import sys

from subprocess import call
from numpy import *
from pylab import *


def openFiles(name1, name2, name3):
	runso = open(name1 + ".cat", "r")
	run = open(name1 + ".txt", "w")

	gunso = open(name2 + ".cat", "r")
	gun = open(name2 + ".txt", "w")

	iunso = open(name3 + ".cat", "r")
	iun = open(name3 + ".txt", "w")

	while True:
		line = runso.readline()
		if not line: break
		if (line[0] != '#'):
			run.write(line)
	run.close()
	runso.close()

	while True:
		line = gunso.readline()
		if not line: break
		if (line[0] != '#'):
			gun.write(line)
	gun.close()
	gunso.close()

	while True:
		line = iunso.readline()
		if not line: break
		if (line[0] != '#'):
			iun.write(line)
	iun.close()
	iunso.close()

	return 

def makePlot(catalog):
	r = catalog[:,1]
	g = catalog[:,7]
	i = catalog[:,8]

	plt.plot(g-i, i, marker = 'o', linestyle='none');
	ax = gca()
	ax.set_ylim(ax.get_ylim()[::-1])
	plt.xlabel("g'-i'")
	plt.ylabel("i'")
	savefig('CMD.pdf')

	return

def main():
	# Files to work on.
	name1 = sys.argv[1]     # r' filter
	name2 = sys.argv[2]     # g' filter
	name3 = sys.argv[3]     # i' filter
	catalog = sys.argv[4]   # Name of the system

	openFiles(name1, name2, name3)

	# Call and excute the binary that cross-correlates the catalogs
	call(["./MatchedCatalog.out", name1 + ".txt", name2 + ".txt", name3 + ".txt"])

	# Rename the cross-correlated catalog to specify the sytem. Read in data and plot.
	call(["mv", "MatchedCatalog.txt", catalog + ".txt"])
	catalog = np.loadtxt(catalog + ".txt")

	makePlot(catalog)

if __name__ == "__main__":
	main()
