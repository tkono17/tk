#!/usr/bin/env python
#---------------------------------------------------------------------
# setup_job.py
#---------------------------------------------------------------------
import os, sys
import re
import getopt
import agt
import aat

def usage():
    print 'Usage: %s <jobconf_file>' % sys.argv[0]
    
def decodeArgs(argv):
    (opts, args) = getopt.getopt(argv[1:], 'h')
    if len(args)>0:
        jobconf_file=args[0]
        return (True, jobconf_file)
    else:
        return (False, '')
    
if __name__=='__main__':
    (status, jobconf_file) = decodeArgs(sys.argv)
    if not status:
        usage()
        sys.exit(-1)
    #
    jc = aat.JobConf()
    jc.read(jobconf_file)
    dataset_name = jc.Dataset.name()
    if dataset_name == '':
        print 'Dataset name in %s is empty' % jobconf_file
        sys.exit(1)
    print 'dataset = ', dataset_name
    agt.createFilelistForDS(dataset_name, agt.FileList_SiteLFNPFN)
    agt.createFilelistToSubmit(agt.FileList_SiteLFNPFN, 'tosubmit.txt')
    agt.setupJobs()
