#!/usr/bin/python2.2
import sys
import os
import zcard
import zjm

def usage():
    print """Usage: mk_zes_jobs lumi_file jobinfo_file header
  lumi_file = runlist file available on the ZEUS lumi page.
  jobinfo   = .jobinfo file.
  header    = common suffix for this job.

Example: > mk_zes_jobs epruns00p.txt 00p charmjet_zes.jobinfo"""

if len(sys.argv)!=3 and len(sys.argv)!=4:
    usage()
else:
    print 'Making ZES control.cards from ', sys.argv[1], 'and',\
    sys.argv[2]
    header = os.path.basename(os.getcwd())
    if len(sys.argv)>3: header = sys.argv[3]
    print 'Header for the jobs : ', header
#    zcard.mk_zes_cards(sys.argv[1], header)
#    print 'Making subdirectories and updating jobinfo file.'
#    zjm.mk_dir_cards(sys.argv[2])

