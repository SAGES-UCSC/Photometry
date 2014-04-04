'''
    Read an FSPS spec file
    '''

class specmodel:
    def __init__(self, attr, wave, flux):
        self.age = attr[0]
        self.mass = attr[1]
        self.lbol= attr[2]
        self.sfr= attr[3]
        self.wave = wave
        self.flux = flux

class readspec:
    def __init__(self, fname):
        self.data = open(fname, "r")
        # Burn header
        while True:
            line = self.data.readline()
            if line[0] != '#':
                break
        
        cols = line.split()
        self.tstep = float(cols[0])
        self.sdim = float(cols[1])
        
        # Get wavelength
        line = self.data.readline()
        cols = line.split()
        self.wave = map(lambda col: float(col), cols)
    
    def next(self):
        line = self.data.readline()
        if line == "":
            self.data.close()
            raise StopIteration()
        
        cols = line.split()
        attr = map(lambda col: float(col), cols)
        
        line = self.data.readline()
        cols = line.split()
        flux = map(lambda col: float(col), cols)
        
        return specmodel(attr, self.wave, flux)
    
    def __iter__(self):
        return self

'''
    For FSPS .mags files
    '''
class FSPSmags:
    def __init__(self, line):
        self.line = line
        cols = line.split()
        self.agegyr    = (10**float(cols[0]) /1e9)
        self.logmass   = float(cols[1])
        self.loglbol   = float(cols[2])
        self.logsfr    = float(cols[3])
        self.V         = float(cols[4])
        self.U         = float(cols[5])
        self.B         = float(cols[6])
        self.B2        = float(cols[7])
        self.R         = float(cols[8])
        self.I         = float(cols[9])
        self.CFHT_B    = float(cols[10])
        self.CFHT_R    = float(cols[11])
        self.CFHT_I    = float(cols[12])
        self.TWOMASS_J  = float(cols[13])
        self.TWOMASS_H  = float(cols[14])
        self.TWOMASS_K  = float(cols[15])
        self.SDSS_U    = float(cols[16])
        self.SDSS_G    = float(cols[17])
        self.SDSS_R    = float(cols[18])
        self.SDSS_I    = float(cols[19])
        self.SDSS_Z    = float(cols[20])
        self.WFPC2_F255W = float(cols[21])
        self.WFPC2_F300W = float(cols[22])
        self.WFPC2_F336W = float(cols[23])
        self.WFPC2_F439W = float(cols[24])
        self.WFPC2_F450W = float(cols[25])
        self.WFPC2_F555W = float(cols[26])
        self.WFPC2_F606W = float(cols[27])
        self.WFPC2_F814W = float(cols[28])
        self.WFPC2_F850LP = float(cols[29])
        self.ACS_F435W  = float(cols[30])
        self.ACS_F475W  = float(cols[31])
        self.ACS_F555W  = float(cols[32])
        self.ACS_F606W  = float(cols[33])
        self.ACS_F625W  = float(cols[34])
        self.ACS_F775W  = float(cols[35])
        self.ACS_F814W  = float(cols[36])
        self.ACS_F850LP = float(cols[37])
        self.UVIS_F218W = float(cols[38])
        self.UVIS_F225W = float(cols[39])
        self.UVIS_F275W = float(cols[40])
        self.UVIS_F336W = float(cols[41])
        self.UVIS_F390W = float(cols[42])
        self.UVIS_F438W = float(cols[43])
        self.UVIS_F475W = float(cols[44])
        self.UVIS_F555W = float(cols[45])
        self.UVIS_F606W = float(cols[46])
        self.UVIS_F775W = float(cols[47])
        self.UVIS_F814W = float(cols[48])
        self.UVIS_F850LP = float(cols[49])
        self.WFC3_F098M = float(cols[50])
        self.WFC3_F105W = float(cols[51])
        self.WFC3_F110W = float(cols[52])
        self.WFC3_F125W = float(cols[53])
        self.WFC3_F140W = float(cols[54])
        self.WFC3_F160W = float(cols[55])
        self.RAC1      = float(cols[56])
        self.IRAC2     = float(cols[57])
        self.IRAC3     = float(cols[58])
        self.IRAC4     = float(cols[59])
        self.ISAAC_K   = float(cols[60])
        self.FORS_V    = float(cols[61])
        self.FORS_R    = float(cols[62])
        self.NICMOS_F110W = float(cols[63])
        self.NICMOS_F160W = float(cols[64])
        self.GALEX_FUV     = float(cols[65])
        self.GALEX_NUV     = float(cols[66])
        self.DES_G         = float(cols[67])
        self.DES_R         = float(cols[68])
        self.DES_I         = float(cols[69])
        self.DES_Z         = float(cols[70])
        self.DES_Y         = float(cols[71])
        self.WFCAM_Z       = float(cols[72])
        self.WFCAM_Y       = float(cols[73])
        self.WFCAM_J       = float(cols[74])
        self.WFCAM_H       = float(cols[75])
        self.WFCAM_K       = float(cols[76])
        self.STEIDEL_UN    = float(cols[77])
        self.STEIDEL_G     = float(cols[78])
        self.STEIDEL_RS    = float(cols[79])
        self.STEIDEL_I     = float(cols[80])
        self.MEGACAM_U     = float(cols[81])
        self.MEGACAM_G     = float(cols[82])
        self.MEGACAM_R     = float(cols[83])
        self.MEGACAM_I     = float(cols[84])
        self.MEGACAM_Z     = float(cols[85])
        self.WISE_W1       = float(cols[86])
        self.WISE_W2       = float(cols[87])
        self.WISE_W3       = float(cols[88])
        self.WISE_W4       = float(cols[89])
        self.UVOT_W2       = float(cols[90])
        self.UVOT_M2       = float(cols[91])
        self.UVOT_W1       = float(cols[92])
        self.MIPS_24       = float(cols[93])
        self.MIPS_70       = float(cols[94])
        self.MIPS_160      = float(cols[95])
        self.SCUBA_450     = float(cols[96])
        self.SCUBA_850     = float(cols[97])
        self.PACS_70       = float(cols[98])
        self.PACS_100      = float(cols[99])
        self.PACS_160      = float(cols[100])
        self.SPIRE_250     = float(cols[101])
        self.SPIRE_350     = float(cols[102])
        self.SPIRE_500     = float(cols[103])
        self.IRAS_12       = float(cols[104])
        self.IRAS_25       = float(cols[105])
        self.IRAS_60       = float(cols[106])
        self.IRAS_100      = float(cols[107])
        self.BESSELL_L     = float(cols[108])
        self.BESSELL_L_PRIME = float(cols[109])
        self.BESSELL_M     = float(cols[110])
        self.STROMGREN_U   = float(cols[111])
        self.STROMGREN_V   = float(cols[112])
        self.STROMGREN_B   = float(cols[113])
        self.STROMGREN_Y   = float(cols[114])
        self.M1500         = float(cols[115])
        self.M2300         = float(cols[116])
        self.M2800         = float(cols[117])

