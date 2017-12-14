#!/usr/bin/python2.2
import os
import sys
import string
import zcard

epruns_96p = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns96p.txt'
epruns_97pp = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns97p.txt'
epruns_98e = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns98e.txt'
epruns_99e = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns99e.txt'
epruns_99p = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns99p.txt'
epruns_00p = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns00p.txt'

epruns_03p = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns03p.txt'
epruns_03p_mvd = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns03p_mvd.txt'
epruns_03p_mvdstt = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns03p_mvdstt.txt'
epruns_04p = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns04p.txt'
epruns_04p_mvd = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns04p_mvd.txt'
epruns_04p_mvdstt = '/datadisk/atlasdata2/kohno/zeus/job/doc/runlist/epruns04p_mvdstt.txt'



if __name__ == '__main__':
    zcard.mk_zes_cards(epruns_98e, '98e')
    zcard.mk_zes_cards(epruns_99e, '99e')
    zcard.mk_zes_cards(epruns_99p, '99p')
    zcard.mk_zes_cards(epruns_00p, '00p')

