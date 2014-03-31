##
Alexa Villaume, for the SAGES group based at UC Santa Cruz


##PURPOSE:
Let's begin with what this is **not** intended to be. This is not intended to be a pipeline for photometry. Given the often heterogeneous nature of
the data we use and the manifold results or end products we can get it is not feasible to make a pipeline that would be generally useful. Instead
this is meant to be a set of tools to make doing photometry quicker, with less scripts being written by us individually, and to set a uniform
general method that holds up the current best methods. Our goals are:
* Make DEIMOS mask design easier and more uniform
* Get the best photometry that we can from our Subaru images. I will be following the methods of Whitaker et al. (2011)
* Mitigate the complications and annoyances that come with working with multiple different catalogs from different sources including archival
  catalogs 

#### Getting and using these tools

To come later. 

##GORY DETAILS:
The basis for most of the routines are treating the sources in each catalog as objects. Look at **Sources.py** to get idea of this. Basically, in
any given routine, such as **makeDSIMinput.py**, when a catalog is read each line is read in as an object. This makes handling each data set and
interchanging between data sets much easier and concise. If you have a catalog that doesn't fit the format of any of the source classes already in
**Sources.py** it's easy to make one just following the format of the source classes already created.


### Routines and functions:

#### Foundational:

* **Sources.py** - This holds each catalog class. Feel free to make your own.

* **phot_utils.py** - A collection of useful photometry functions to be included in larger programs.
    * **correctMag** - Input: a catalog of source objects and a correction factor.
    * **makeMagCut** - Input: A magnitude, low, and high. Returns boolean.
    * **makeColorCut** - This function takes a predetermined line in color-color space and makes a cut based on that and how generous we wish to
      be. Input: Four magnitude colors (mag1, mag2, mag3, mag4), line parameters(x0, x1, m, b), and the value for how generous the cut shoud be (var)
    * **detSizeCut** - Intended to cut out all but the point sources from a data set. Input: The a_world column from the catalog and the number of
      bins.
    * **LookeAtShapes** - I'm uncertain about the above's robustness so this is a function to look at the histogram of the a_world values. 
    * **calcMedian** - Input: list of values Output: median of the list 
    * **calcMAD** - Input: List of values Output: median absolute deviation
    * **nohHead** -  Burn the header of an input file. Input: A catalog Output: All the lines that aren't comments

* **geom_utils.pyt** - A collection of useful geometry functions to have on hand for larger programs
    * **calcY** - Input: x, m, b Output: y
    * **inBox** - Test whether a point is in a box. Input: Bounds of box (x0, x1, y0, y1), point coordinates(px, py) Output: Boolean
    * **makeRadiusCut** - Make cut on data for a given radius. Does not take into account projection effects. Input: Point coordinates (ra, dec) center coordinates (gal_ra, gal_dec), distance. All inputs in degress. Output: Boolean
    * **intersecting** - Test whether two boxes are interesecting. Input: Bounds of Box1, bounds of Box2 Output: Bolean 
    * **norm** - Calculate the norm between two points.
    * **norm2** - Calculate the square of the norm between two points
    * **clip_box** - Trim a box dimensions 

* **Quadtree.py** - A way to index sources in two dimensions in order to cross-correlate catalogs. There is a C-version of this (in MakeCatalog). It
  runs much faster but you lose the object oriented-ness that makes the Python version so easy to use. 

#### Mask Making:

* **simple_test.py** - This program demonstrates how to put together various routines and functions to do some basic GC candidate selection.
  This program starts with an already cross-correlated final catalog of all a given system. You can tweak the input to the various functions to cut
  down the original catalog to a catalog of GC candidates using the functions from **geom_utils.py** and **phot_utils.py**. 

* **makeDSIMin.py** - A program to turn a catalog file into a DSIM input file.

    **Calling Sequence:** python makeDSIM.py <'Input Catalog'> <'Output Name'>

    **What you have to edit:** 
    * Lines 23-27 - need to be changed to suit the needs of the mask design
    * Line 31 - Need to change the kind of the class the catalog belongs to
    * Line 40, 47 - Change src.mag1 to whatever the proper magnitude column is


  **What you have to edit:**
  * Line 12 - Change the class the catalog belongs to


**NOTE:** There are some other DSIM/mask making routines in the DSIM repo. They were written before I had implemented the object oriented parts of
  these tools and I'm working on updating them.


#### Photometry:

These will be the set of routines that will allow to extract the photometry from images.

* **createSexConfig.py** - Generate a Source Extractor configuration file. This is intended to be included as a function in a larger program. Now the
  inputs are fairly rudimentry.
* **createSexParam.py** - Generate a Source Extractor configuration file. This is intended to be included as a function in a larger proram.
* **findBestAperture.py** - The first part of reconstructing the methods of Whitaker et al. (2011). This is a routine to optimize the aperture we use
  for extracting photometery. Not fully functional yet.
* **makeRegionFile.py** - Turn a catalog into a DS9 regions file. This is written as a function to be included in a larger program, it's not to be run
  from the command line.

#### To-Do:

[] Finish findBestAperture.py
[] Write findZeropoint.py 
[] Fix correctMag
[] Fix magCut
[] Refine UX
[] Get Lee to resend PSF code
[] Coordinate matching?
[] Completeness 
[] GC Candidate Likelihood
