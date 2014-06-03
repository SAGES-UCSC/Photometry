#!/usr/bin/env python
import sys, os, commands, math, string
from os import path
#os.system('cp -f ~/login.cl .'); from pyraf import *
import pyfits as pf

def create_sex_config(b,infile,weight,paramfile,assoc):
	config = b+'.config'
	seeing = commands.getoutput('gethead '+infile+' SEEING')
	seeing = '1.2'
	#seeing = commands.getoutput('gethead '+infile+' MFWHM ')
	#print 'FIX SEEING'
	zp = commands.getoutput('gethead '+infile+' MAGZP')
	#zp = '26.855'
	#print 'FIX MAGZP'
	gain = commands.getoutput('gethead '+infile+' TEXPTIME')

	print 'running on ',infile,' with weight:',weight,', gain:',gain,' zp:',zp,' seeing:',seeing


	fout = open(config,'w')
	fout.write("""# Default configuration file for SExtractor 2.8.6
# EB 2011-03-01
#

#-------------------------------- Catalog ------------------------------------

CATALOG_NAME     """+b+""".cat       # name of the output catalog
CATALOG_TYPE     ASCII_HEAD     # NONE,ASCII,ASCII_HEAD, ASCII_SKYCAT,
                                # ASCII_VOTABLE, FITS_1.0 or FITS_LDAC
PARAMETERS_NAME  """+paramfile+"""  # name of the file containing catalog contents

#------------------------------- Extraction ----------------------------------

DETECT_TYPE      CCD            # CCD (linear) or PHOTO (with gamma correction)
DETECT_MINAREA   5              # minimum number of pixels above threshold
THRESH_TYPE      RELATIVE       # threshold type: RELATIVE (in sigmas)
                                # or ABSOLUTE (in ADUs)
DETECT_THRESH    1.2            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2
ANALYSIS_THRESH  1.2            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2

FILTER           Y              # apply filter for detection (Y or N)?
FILTER_NAME      gauss_4.0_7x7.conv   # name of the file containing the filter
FILTER_THRESH                   # Threshold[s] for retina filtering

DEBLEND_NTHRESH  32             # Number of deblending sub-thresholds
DEBLEND_MINCONT  0.005          # Minimum contrast parameter for deblending

CLEAN            Y              # Clean spurious detections? (Y or N)?
CLEAN_PARAM      1.0            # Cleaning efficiency

MASK_TYPE        CORRECT        # type of detection MASKing: can be one of
                                # NONE, BLANK or CORRECT

#-------------------------------- WEIGHTing ----------------------------------

WEIGHT_TYPE      MAP_WEIGHT,MAP_WEIGHT           # type of WEIGHTing: NONE, BACKGROUND,
                                # MAP_RMS, MAP_VAR or MAP_WEIGHT
WEIGHT_IMAGE     """+weight+"""    # weight-map filename
WEIGHT_GAIN      Y              # modulate gain (E/ADU) with weights? (Y/N)
WEIGHT_THRESH                   # weight threshold[s] for bad pixels

#-------------------------------- FLAGging -----------------------------------

FLAG_IMAGE       flag.fits      # filename for an input FLAG-image
FLAG_TYPE        OR             # flag pixel combination: OR, AND, MIN, MAX
                                # or MOST

#------------------------------ Photometry -----------------------------------

PHOT_APERTURES    10 #13.3 #20 #10 #12.5           #9.375              # MAG_APER aperture diameter(s) in pixels
PHOT_AUTOPARAMS  2.5, 3.       # MAG_AUTO parameters: <Kron_fact>,<min_radius>
PHOT_PETROPARAMS 2.0, 3.5       # MAG_PETRO parameters: <Petrosian_fact>,
                                # <min_radius>
PHOT_AUTOAPERS   3.0,3.0        # <estimation>,<measurement> minimum apertures
                                # for MAG_AUTO and MAG_PETRO
PHOT_FLUXFRAC    0.5            # flux fraction[s] used for FLUX_RADIUS

SATUR_LEVEL      5000000000000000000.0        # level (in ADUs) at which arises saturation

MAG_ZEROPOINT    """+zp+"""            # magnitude zero-point
MAG_GAMMA        4.0            # gamma of emulsion (for photographic scans)
GAIN             	"""+gain+"""            # detector gain in e-/ADU
PIXEL_SCALE      0            # size of pixel in arcsec (0=use FITS WCS info)

#------------------------- Star/Galaxy Separation ----------------------------

SEEING_FWHM      """+seeing+"""            # stellar FWHM in arcsec
#STARNNW_NAME     default.nnw    # Neural-Network_Weight table filename

#------------------------------ Background -----------------------------------

BACK_TYPE        AUTO           # AUTO or MANUAL
BACK_VALUE       0.0            # Default background value in MANUAL mode
BACK_SIZE        32             # Background mesh: <size> or <width>,<height>
BACK_FILTERSIZE  3              # Background filter: <size> or <width>,<height>

BACKPHOTO_TYPE   GLOBAL         # can be GLOBAL or LOCAL
BACKPHOTO_THICK  24             # thickness of the background LOCAL annulus
BACK_FILTTHRESH  0.0            # Threshold above which the background-
                                # map filter operates

#------------------------------ Check Image ----------------------------------


CHECKIMAGE_TYPE  BACKGROUND,OBJECTS,SEGMENTATION,-BACKGROUND,MINIBACK_RMS,APERTURES,FILTERED
#CHECKIMAGE_TYPE  NONE           # can be NONE, BACKGROUND, BACKGROUND_RMS,
                                # MINIBACKGROUND, MINIBACK_RMS, -BACKGROUND,
                                # FILTERED, OBJECTS, -OBJECTS, SEGMENTATION,
                                # or APERTURES
#CHECKIMAGE_NAME  check.fits     # Filename for the check-image
CHECKIMAGE_NAME  back.fits,objs.fits,seg.fits,back_sub.fits,miniback_rms.fits,aps.fits,filter.fits

#--------------------- Memory (change with caution!) -------------------------

MEMORY_OBJSTACK  3000           # number of objects in stack
MEMORY_PIXSTACK  300000         # number of pixels in stack
MEMORY_BUFSIZE   1024           # number of lines in buffer

#------------------------------- ASSOCiation ---------------------------------

ASSOC_NAME       assoc.cat       # name of the ASCII file to ASSOCiate
ASSOC_DATA       1,5            # columns of the data to replicate (0=all)
ASSOC_PARAMS     2,3            # columns of xpos,ypos[,mag]
ASSOC_RADIUS     1.0            # cross-matching radius (pixels)
ASSOC_TYPE       NEAREST        # ASSOCiation method: FIRST, NEAREST, MEAN,
                                # MAG_MEAN, SUM, MAG_SUM, MIN or MAX
ASSOCSELEC_TYPE  ALL        # ASSOC selection type: ALL, MATCHED or -MATCHED

#----------------------------- Miscellaneous ---------------------------------

VERBOSE_TYPE     NORMAL         # can be QUIET, NORMAL or FULL
WRITE_XML        N              # Write XML file (Y/N)?
XML_NAME         sex.xml        # Filename for XML output
XSL_URL          .
                                # Filename for XSL style-sheet
NTHREADS         2              # 1 single thread

FITS_UNSIGNED    N              # Treat FITS integer values as unsigned (Y/N)?
INTERP_MAXXLAG   16             # Max. lag along X for 0-weight interpolation
INTERP_MAXYLAG   16             # Max. lag along Y for 0-weight interpolation
INTERP_TYPE      ALL            # Interpolation type: NONE, VAR_ONLY or ALL

#--------------------------- Experimental Stuff -----------------------------

PSF_NAME         default.psf    # File containing the PSF model
PSF_NMAX         9              # Max.number of PSFs fitted simultaneously
PSFDISPLAY_TYPE  SPLIT          # Catalog type for PSF-fitting: SPLIT or VECTOR
SOM_NAME         default.som    # File containing Self-Organizing Map weights


""")
	fout.close()
	return config

def load_file(f):
	verbose = False
        if verbose:
                print '--- loading file ---'
        __hdulist = pf.open(f)
        if verbose:
                __hdulist.info()
                __hdulist[0].data
                __hdulist[0].data.shape
                print '--- loaded file  ---'
        return __hdulist

def gen_filter(out='gauss_4.0_7x7.conv'):
	fout = open(out,'w')
	fout.write("""CONV NORM
# 7x7 convolution mask of a gaussian PSF with FWHM = 4.0 pixels.
0.047454 0.109799 0.181612 0.214776 0.181612 0.109799 0.047454
0.109799 0.254053 0.420215 0.496950 0.420215 0.254053 0.109799
0.181612 0.420215 0.695055 0.821978 0.695055 0.420215 0.181612
0.214776 0.496950 0.821978 0.972079 0.821978 0.496950 0.214776
0.181612 0.420215 0.695055 0.821978 0.695055 0.420215 0.181612
0.109799 0.254053 0.420215 0.496950 0.420215 0.254053 0.109799
0.047454 0.109799 0.181612 0.214776 0.181612 0.109799 0.047454""")
	fout.close()
	return out

	hdu = load_file(psf)
	data = hdu[0].data
	fout.write("""CONV NONNORM
# 5x5 convolution mask of a gaussian PSF with FWHM = 2.0 pixels.
""")

	#print data[23][12]
	#print data[y][x] !!!

	filter = 'Ks_filter.conv'
	for i in range(8,44):
		#fout.write(' '.join(map(str,data[i][18:34]))+'\n')
		fout.write(' '.join(map(str,data[i][8:44]))+'\n')
	fout.close()


def gen_xy_param():
	fout = open('xy.param','w')
	fout.write("""NUMBER
X_IMAGE
Y_IMAGE
FLAGS
""")
	fout.close()
	return 'xy.param'

if __name__ == '__main__':
	filter = gen_filter()

	selband = sys.argv[1]
	imgversion = 'go5'
	imgversion = '0.1'

	find_image='../'+imgversion+'/COSMOS-1_'+selband+'_sci.fits'
	expfiles= '../'+imgversion+'/COSMOS-1_'+selband+'_exp.fits,../'+imgversion+'/COSMOS-1_'+selband+'_exp.fits'
	find_image='../COSMOS-1_'+selband+'_sci.fits'
	expfiles= '../COSMOS-1_'+selband+'_exp.fits,../COSMOS-1_'+selband+'_exp.fits'
	config = create_sex_config(''+selband+'_orig',find_image,expfiles,'fs_v0.1.param',False)
	cmd = 'sex '+find_image+','+find_image+' -c '+config
	os.system(cmd)
	#sys.exit(1)
	catfile = selband+'_orig.cat'
	os.system('create_reg.py '+catfile)
	os.system('load '+find_image)
	os.system('xpaset -p ds9 regions load '+selband+'_orig.reg')

	bands = ['Ks']
	bands = ['Ks','Hl','J1','J2','J3','Hs','NB-1.18','NB-2.09']
	field = 'COSMOS-1'
	for b in bands:
		infile = '../../lucy_match/match_'+imgversion+'/'+field+'_'+b+'.fits'
		expfiles= '../COSMOS-1_'+selband+'_exp.fits,../'+field+'_'+b+'_exp.fits'
		catfile = b+'.cat'

		config = create_sex_config(b,infile,expfiles,'fs_v0.1.param',True)
		cmd = 'sex '+find_image+','+infile+' -c '+config
		print cmd
		os.system(cmd)
		#os.system('create_reg.py '+catfile)
		#os.system('load '+infile)
		#os.system('xpaset -p ds9 regions load '+b+'.reg')

