#!/usr/bin/python2.2
#------------------------------------------------------------------------
# Zeus Job Submitter
#------------------------------------------------------------------------
import os
import re
import zjm

def check_outbox():
    os.chdir(zjm.outbox())
    jobs = os.listdir('.')
    re_jobinfo = re.compile('\.jobinfo')
    re_bak = re.compile('~$')
    for job in jobs:
        if not re_jobinfo.search(job) or re_bak.search(job): continue
        zjm.do_jobsub(job, 1)
    
def run_js():
#    job_sub = JobSubmitter()
    os.chdir(zjm.outbox())
    check_outbox()

if __name__ == '__main__':
    f = zjm.find_jobinfo()
    if f == '':
        print 'No .jobinfo file found'
    else:
        a = "cp %s %s" % (f, zjm.outbox())
        print a
#        os.system(a)
        run_js()

