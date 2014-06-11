##
Alexa Villaume, for the SAGES group based at UC Santa Cruz


####PURPOSE:
Let's begin with what this is **not** intended to be. This is not intended to be a pipeline for photometry. Given the often heterogeneous nature of
the data we use and the manifold results or end products we can get it is not feasible to make a pipeline that would be generally useful. Instead
this is meant to be a set of tools to make doing photometry quicker, with less scripts being written by us individually, and to set a uniform
general method that holds up the current best methods. Our goals are:
* Make DEIMOS mask design easier and more uniform
* Get the best photometry that we can from our Subaru images. I will be following the methods of Whitaker et al. (2011)
* Mitigate the complications and annoyances that come with working with multiple different catalogs from different sources including archival
  catalogs 

#### Things to know

I wrote these routines using python 2.7.6 for a Mac computer. To run them you need to install:

1. [Source Extractor](http://www.astromatic.net/software/sextractor) - There are differences between Source Extractor for Mac and Source
   Extractor for Linux. The call to Soure Extractor is different, so if you're a Linux user be aware of that.

2. Numpy and maplotlib
3. [astropy](http://www.astropy.org/)
4. [astroquery](https://github.com/  astropy/astroquery)

#### Getting and using these tools

The first step is to get git - 

*[Installing git](http://docs.astropy.org/en/stable/development/workflow/git_install.html)

*[Configuring git](http://docs.astropy.org/en/stable/development/workflow/git_configure.html)

*[Git resources](http://docs.astropy.org/en/stable/development/workflow/git_resources.html)


An explanation of the code and how to use it is in the wiki for this repository.

#### Raising an issue AKA Something sucks/Something is confusing/Something needs to be added

If, while trying to use any part of this code, you find that something doesn't work right, as expected, or could be improved you can go the the
"Issues" tab and write a post about it. It can be anything, even if you find an aspect of the documentation confusing. The Issues tab is also the
place to request features. 

