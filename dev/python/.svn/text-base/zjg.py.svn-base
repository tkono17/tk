#!/usr/bin/python2.2
#------------------------------------------------------------------------
# Zeus Job Getter (zjg) module
#------------------------------------------------------------------------
import os
import zjm

def check_sentbox():
    os.chdir(zjm.sentbox())
    jobs = os.listdir('.')
    re_jobinfo = re.compile('\.jobinfo')
    re_bak = re.compile('~$')
    for job in jobs:
        if not re_jobinfo.search(job) or re_bak.search(job): continue
        zjm.do_jobget(job, 1)
    
def run_jg():
#    job_sub = JobGetter()
    os.chdir(zjm.sentbox())
    check_sentbox()

if __name__ == '__main__':
    f = zjm.find_jobinfo()
    if f == '':
        print 'No .jobinfo file found'
    else:
        run_jg()
