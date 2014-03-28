'''
AUTHOR
    Alexa Villaume, UCSC

PUPROSE
    To turn a source catalog into a DSIM compatible input file

CALLING SEQUENCE
    python makeDSIMinput.py <catalog> <output>

'''

import sys
import math
import geom_utils as gu
import phot_utils as pu
import Sources as S

def detPriority(mag_min, value):
    return math.ceil((100 - (100*((value - mag_min)/mag_min))))

def main():
    equinox = 2000
    passband = 'I'
    sample = 1
    s_flag = 1
    pa = 119
    catalog = open(sys.argv[1], 'r')

    tmp = filter(lambda line: pu.noHead(line), catalog)
    src = map(lambda line: S.CFHTSource(line), tmp)
    catalog.close()

    # DSIM requires that RA and DEC be in sexagesimal
    ra = map(lambda obj: pu.convertRA(obj.ra), src)
    dec = map(lambda obj: pu.convertDEC(obj.dec), src)

    # Determine priority for each source
    mag_min = min(map(lambda s: s.mag1, src))
    priority = map(lambda s: detPriority(mag_min, s.mag1), src)

    # Put it all together and write to ouput file
    output = open(sys.argv[2], 'w')
    for i in src:
        output.write('%10s' % src[i].name + '%15s' % ra[i] + '%15s' % dec[i] +
                        '%6.d' % equinox + '%10.2f' % src[i].mag1 + '%2s' % passband +
                        '%5.0d' % priority[obj] + '%5.0d' % sample + '%5s' % s_flag +
                        '%10.d' % pa + '\n')
    output.close()

if __name__ == '__main__':
    sys.exit(main())
