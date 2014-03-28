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
* makeDSIMin.py - A program to turn a catalog file into a DSIM input file.

**Calling Sequence:** python makeDSIM.py <'Input Catalog'> <'Output Name'>

**Things you have to edit:** 
* Lines 23-27 - need to be changed to suit the needs of the mask design
* Line 31 - Need to change the kind of the class the catalog belongs to
* Line 40, 47 - Change src.mag1 to whatever the proper magnitude column is 
