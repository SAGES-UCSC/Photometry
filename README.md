##AUTHOR:
Alexa Villaume, for the SAGES group based at UC Santa Cruz

##PURPOSE:
This is intended to be a set of tools that will make doing photometry both easier and more uniform across the SAGES group. These are the following
goals:
* Make DEIMOS mask design easier and more uniform
* Get the best photometry that we can from our Subaru images. I will be following the methods of Whitaker et al. (2011)
* Mitigate the complications and annoyances that come with working with multiple different catalogs from different sources including archival
  catalogs 


##EXPLANATION:
The basis for most of the routines are treating the sources in each catalog as objects. Look at **Sources.py** to get idea of this. Basically, in
any given routine, such as **makeDSIMinput.py**, when a catalog is read each line is read in as an object. This makes handling each data set and
interchanging between data sets much easier and concise. If you have a catalog that doesn't fit the format of any of the source classes already in
**Sources.py** it's easy to make one just following the format of the source classes already created.


### Routines and functions:
* **phot_utils.py** - A collection of useful photometry functions to be included in larger programs.
    * **correctMag** - Input: a catalog of source objects and a correction factor.
    * **makeMagCut** - Input: A magnitude, low, and high. Returns boolean.
    * **makeColorCut** - 
    * **detSizeCut** -
    * **LookeAtShapes** -
    * **calcMedian** - Input: list of values Output: median of the list 
    * **calcMAD** - Input: List of values Output: median absolute deviation
    * **nohHead** -  Input: A catalog Output: All the lines that aren't comments

* **geom_utils.pyt** - A collection of useful geometry functions to have on hand for larger programs
    * **calcY** - Input: x, m, b Output: y
    * **inBox** - Test whether a point is in a box. Input: Bounds of box (x0, x1, y0, y1), point coordinates(px, py) Output: Boolean
    * **makeRadiusCut** - Make cut on data for a given radius. Does not take into account projection effects. Input: Point coordinates (ra, dec) center coordinates (gal_ra, gal_dec), distance. All inputs in degress. Output: Boolean
    * **intersecting** - Test whether two boxes are interesecting. Input: Bounds of Box1, bounds of Box2 Output: Bolean 
    * **norm** - Calculate the norm between two points.
    * **norm2** - Calculate the square of the norm between two points
    * **clip_box** - Trim a box dimensions 

* **makeDSIMin.py** - A program to turn a catalog file into a DSIM input file.

    **Calling Sequence:** python makeDSIM.py <'Input Catalog'> <'Output Name'>

    **What you have to edit:** 
    * Lines 23-27 - need to be changed to suit the needs of the mask design
    * Line 31 - Need to change the kind of the class the catalog belongs to
    * Line 40, 47 - Change src.mag1 to whatever the proper magnitude column is

* **makeRegionFile.py** - Turn a catalog into a DS9 regions file. This is written as a function to be included in a larger program, it's not to be run
  from the command line.

  **What you have to edit:**
  * Line 12 - Change the class the catalog belongs to
