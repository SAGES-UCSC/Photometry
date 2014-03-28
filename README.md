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
interchanging between data sets much easier and concise.
