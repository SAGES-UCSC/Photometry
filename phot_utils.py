import math


'''
All of these inputs need to be in degrees.
'''
def makeRadiusCut(ra, dec, gal_ra, gal_dec, distance):
    if (math.sqrt((ra-gal_ra)**2) + math.sqrt((dec-gal_dec)**2)) <= distance:
        return 1
    else:
        return 0

def makeColorCut():


def makeShapeCut():

def testRadiusCut():

def testColorCut():
