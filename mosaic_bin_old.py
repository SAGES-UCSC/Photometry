import asciitable, tgen
import numpy as np
import fetch_swarp as fsw
import pyfits as pf

clean_list = False
gstitch = True
imcrop = False
immask = False
imbin = False

if (immask):
    from pyraf import iraf
    import pylipse

if (clean_list):
    gals = asciitable.read('../tully.dat')
    f = open('../tully_sdss.dat','w')
    f.write('# gname ra dec b_mag d_mpc\n')
else:
    gals = asciitable.read('sluggs_gals.dat')

winlist = pf.getdata('window_flist.fits')
cols = ['g','r','i']
dx, dy = 3000, 3000
mdr = 0.4

for g in range(np.size(gals['gname'])):
#for g in range(1):
    gn = gals['gname'][g]

    if (clean_list):
        radec = tgen.radec_deg(gals['ra_h'][g], gals['ra_m'][g], 0.0,
                               gals['dec_d'][g], gals['dec_m'][g], 0.0)
        wfields = ((winlist['RA'] > radec[0]-mdr) &
                   (winlist['RA'] < radec[0]+mdr) &
                   (winlist['DEC'] > radec[1]-mdr) &
                   (winlist['DEC'] < radec[1]+mdr))
        if np.sum(wfields) > 0:
            f.write(gn+' '+str('{:7.3f}').format(radec[0])+' '+
                    str('{:7.3f}').format(radec[1])+' '+
                    str('{:7.2f}').format(gals['b_mag'][g])+' '+
                    str('{:5.1f}').format(gals['d_mpc'][g])+'\n')

    for c in range(np.size(cols)):
# fetch field images and stitch them
        if (gstitch):
            fsw.fetch_files(None, [gals['ra'][g],gals['dec'][g]],
                            dr=mdr, band=cols[c],
                            outdir='/galaxies/'+gn+'/frames')
            fsw.stitch(fdir='/galaxies/'+gn+'/frames', band=cols[c],
                       verbose=False, sub_bg=False,
                       cadir='/galaxies/'+gn+'/coadds')

# crop
        if (imcrop):
            img = pf.getdata('../galaxies/'+gn+'/coadds/coadd_'+cols[c]+'.fits')
            wht = pf.getdata('../galaxies/'+gn+'/coadds/coadd_'+
                             cols[c]+'.wht.fits')
            xcen, ycen = int(img.shape[0]/2), int(img.shape[1]/2)

            cr_img = tgen.crop(img, xcen-dx, xcen+dx, ycen-dy, ycen+dy)
            cr_wht = tgen.crop(wht, xcen-dx, xcen+dx, ycen-dy, ycen+dy)

# save cropped
            pf.writeto('../galaxies/'+gn+'/_c_'+cols[c]+'.fits',cr_img)
            pf.writeto('../galaxies/'+gn+'/_c_'+cols[c]+'.wht.fits',cr_wht)

# mask
    if (immask):
        pfix = '../galaxies/'+gn+'/_c_'
        fsw.objmask([pfix+'g.fits',pfix+'r.fits',pfix+'i.fits'],
                    [pfix+'g.wht.fits',pfix+'r.wht.fits',pfix+'i.wht.fits'],
                    outdir='../galaxies/'+gn, tfdel=False)

# bin
    if (imbin):
        omask = pf.getdata('../galaxies/'+gn+'/omask_comb.fits')
        wmask = (omask == 1)

        for c in range(np.size(cols)):
            cr_img = pf.getdata('../galaxies/'+gn+'/sh_img_'+str(c)+'.fits')
            cr_img[wmask] = -99.0
            bimg = tgen.binarr(cr_img, 10, zval=-99.0)

# save binned mosaic
            pf.writeto('../galaxies/'+gn+'/binned_'+cols[c]+'.fits',bimg)

if (clean_list):
    f.close()
