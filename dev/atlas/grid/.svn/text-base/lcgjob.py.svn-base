#!/usr/bin/env python
#---------------------------------------------------------------------
# lcgjob.py
#---------------------------------------------------------------------
import os, sys
import re
import getopt
import agt
import aat
import alt

def usage():
    """Usage"""
    print 'Usage: %s [options]' % sys.argv[0]
    print """------
Options: -c <jobconf> ... Job configuration file [jobconf.txt]
         -p           ... Prepare jobs
         -r           ... Run jobs
         -s           ... Query status of jobs
         -g           ... Get jobs
         -d           ... Delete jobs
         -j <jobid>   ... Only for the specified jobid
         -l <joblist> ... A file with a list of job IDs [joblist]
         -h           ... Help
"""

class pars:
    job_conf = ''
    job_id = ''
    job_list = ''
    do_prepare = False
    do_run = False # or submit
    do_get = False
    do_status = False
    do_delete = False
    verbose = False
    def ok(cls):
        if len(pars.job_conf)>0: return True
        else: return False
    ok = classmethod(ok)
    def printIt(cls):
        print 'Job configuration: %s' % pars.job_conf
        print 'Job id           : %s' % pars.job_id
        print 'Job list         : %s' % pars.job_list
        print 'Do prepare       :', pars.do_prepare
        print 'Do run           :', pars.do_run
        print 'Do status        :', pars.do_status
        print 'Do get           :', pars.do_get
        print 'Do delete        :', pars.do_delete
        print 'Verbose          :', pars.verbose
    printIt = classmethod(printIt)
    
if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], 'hprsgc:j:vl:')
    for (opt, value) in opts:
        if opt in ['-h']:
            usage()
            sys.exit(1)
        elif opt in ['-p']:
            pars.do_prepare = True
        elif opt in ['-r']:
            pars.do_run = True
        elif opt in ['-s']:
            pars.do_status = True
        elif opt in ['-g']:
            pars.do_get = True
        elif opt in ['-c']:
            pars.job_conf = value
        elif opt in ['-j']:
            pars.job_id = value
        elif opt in ['-l']:
            pars.job_list = value
        elif opt in ['-v']:
            pars.verbose = True
    if not pars.ok():
        usage()
        sys.exit(2)
    if pars.verbose: pars.printIt()
    #
    jm = agt
    #
    agt.agtlog = '%s/logs/agt.log' % os.getcwd()
    alt.altlog = '%s/logs/alt.log' % os.getcwd()
    aat.aatlog = '%s/logs/aat.log' % os.getcwd()
    jc = aat.JobConf()
    jc.read(pars.job_conf)
    if jc.JobType.name() == 'LXBATCH': jm = alt
    if pars.job_id!='':
        jobs = pars.job_id.split(',')
        curdir = os.getcwd()
        for jid in jobs:
            if os.path.isdir(jid):
                os.chdir(jid)
                if pars.do_prepare: jm.prepareJob(jc)
                if pars.do_run: jm.runJob(jc)
                if pars.do_status: jm.statusJob(jc)
                if pars.do_get: jm.getJob(jc)
                os.chdir(curdir)
    elif pars.job_id=='' and pars.job_list!='':
        if pars.do_prepare: jm.prepareJobs(jc, pars.job_list)
        if pars.do_run: jm.runJobs(jc, pars.job_list)
        if pars.do_status: jm.statusJobs(jc, pars.job_list)
        if pars.do_get: jm.getJobs(jc, pars.job_list)
    else:
        print 'Neither job_id nor job_list were non-nill. No action taken'
