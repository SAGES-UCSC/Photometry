"""
Create a source extractor configuration file based on input parameters.

Need to include aperture stuff
"""

def createSexConfig(name, filter_file, param_file,  assoc_file, ap, doassoc):
    config = name + '.config'

    if doassoc == True:
        aname = "ASSOC_NAME"
        adata = "ASSOC_DATA"
        aparam = "ASSOC_PARAMS"
        aradius = "ASSOC_RADIUS"
        atype = "ASSOC_TYPE"
        aselec = "ASSOCSELEC_TYPE"
    else:
        aname = "#ASSOC_NAME"
        adata = "#ASSOC_DATA"
        aparam = "#ASSOC_PARAMS"
        aradius = "#ASSOC_RADIUS"
        atype = "#ASSOC_TYPE"
        aselec = "#ASSOCSELEC_TYPE"

    ap = str(ap)
    seeing = str(1.2)
    zp = str(0)            # Going to correct zeropoints after the final catalog is made
    gain = str(2.5)        # From the Subaru S-Cam website
    fout = open(config,'w')
    fout.write("""
                    #

                    #-------------------------------- Catalog ------------------------------------

                    CATALOG_NAME     """+name+""".cat       # name of the output catalog
                    CATALOG_TYPE     ASCII_HEAD     # NONE,ASCII,ASCII_HEAD, ASCII_SKYCAT,
                    # ASCII_VOTABLE, FITS_1.0 or FITS_LDAC
                    PARAMETERS_NAME  """+param_file+"""  # name of the file containing catalog contents

                    #------------------------------- Extraction ----------------------------------

                    DETECT_TYPE      CCD            # CCD (linear) or PHOTO (with gamma correction)
                    DETECT_MINAREA   5              # minimum number of pixels above threshold
                    DETECT_THRESH    1.2            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2
                    ANALYSIS_THRESH  1.2            # <sigmas> or <threshold>,<ZP> in mag.arcsec-2

                    FILTER           Y              # apply filter for detection (Y or N)?
                    FILTER_NAME      """+filter_file+"""   # name of the file containing the filter

                    DEBLEND_NTHRESH  32             # Number of deblending sub-thresholds
                    DEBLEND_MINCONT  0.005          # Minimum contrast parameter for deblending

                    CLEAN            Y              # Clean spurious detections? (Y or N)?
                    CLEAN_PARAM      1.0            # Cleaning efficiency

                    MASK_TYPE        CORRECT        # type of detection MASKing: can be one of
                    # NONE, BLANK or CORRECT


                    #-------------------------------- FLAGging -----------------------------------

                    FLAG_IMAGE       flag.fits      # filename for an input FLAG-image
                    FLAG_TYPE        OR             # flag pixel combination: OR, AND, MIN, MAX
                    # or MOST

                    #------------------------------ Photometry -----------------------------------

                    PHOT_APERTURES """+ap+"""       # MAG_APER aperture diameter(s) in pixels
                    PHOT_AUTOPARAMS  2.5, 3.        # MAG_AUTO parameters: <Kron_fact>,<min_radius>
                    PHOT_PETROPARAMS 2.0, 3.5       # MAG_PETRO parameters: <Petrosian_fact>,
                    # <min_radius>
                    PHOT_AUTOAPERS   3.0,3.0        # <estimation>,<measurement> minimum apertures
                    # for MAG_AUTO and MAG_PETRO
                    PHOT_FLUXFRAC    0.5            # flux fraction[s] used for FLUX_RADIUS

                    SATUR_LEVEL      5000000000000000000.0        # level (in ADUs) at which arises saturation

                    MAG_ZEROPOINT     """+zp+"""            # magnitude zero-point
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

                    """+aname+"""       """+assoc_file+"""       # name of the ASCII file to ASSOCiate
                    """+adata+"""    1,2            # columns of the data to replicate (0=all)
                    """+aparam+"""     1,2            # columns of xpos,ypos[,mag]
                    """+aradius+"""     2.0            # cross-matching radius (pixels)
                    """+atype+"""       NEAREST        # ASSOCiation method: FIRST, NEAREST, MEAN,
                    # MAG_MEAN, SUM, MAG_SUM, MIN or MAX
                    """+aselec+"""  MATCHED        # ASSOC selection type: ALL, MATCHED or -MATCHED

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
