'''
AUTHOR
    Alexa Villaume, UCSC

PURPOSE
    Make a radius cut given a center and a maximum distance

INPUT PARAMETERS
    The name of the system
    Path to catalog
    Column the ra values are in
    Column the dec values are in
    Center coordinates in degree
    Distance to make the cut

FILES CREATED
    New catalog of the form <system name> + "_radiuscut"

NOTES
    This is going to be rewritten so it can be easily included in
    larger programs

'''


import math

def makeCut(ra, dec, gal_ra, gal_dec, distance):
    if (math.sqrt((ra-gal_ra)**2) + math.sqrt((dec-gal_dec)**2)) <= distance:
        return 1
    else:
        return 0


def main():
    galaxy = raw_input("Name of galaxy? ")
    name = raw_input("Name of catalog to make cuts on? ")
    ra_col = int(raw_input("Column that RA values are in: "))
    dec_col = int(raw_input("Column that dec values are in: "))
    gal_ra = float(raw_input("RA of galaxy center (deg)? "))
    gal_dec = float(raw_input("DEC of galaxy center (deg)? "))
    distance = float(raw_input("Distance to make cut at (deg)? "))

    output = open(galaxy + "_radiuscut.txt", "w")
    with open(name, "r") as f:
        for object in (raw.strip().split() for raw in f):
            if  makeCut(float(object[ra_col]), float(object[dec_col]), gal_ra, gal_dec, distance):
                output.write("%10s" % object[0] + "%15s" % object[1] +  "%15s" % object[2]
                + "%15s" % object[3] + "%15s" % object[4] + "%15s" % object[5] + "%15s" % object[6]
                + "%15s" % object[7] + "%15s" % object[8] + "%15s" % object[9] + "%15s" % object[10]
                + "%15s" % object[11] + "%15s" % object[12] + "\n")

if __name__ == "__main__":
    main()
