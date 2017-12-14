#!/usr/bin/env python
#----------------------------------------------------------------------
# alt.py
#--------
# ATLAS lxbatch tools
#----------------------------------------------------------------------
import os, sys
import re
import commands
import tklog

altlog = 'logs/alt.log'


def jobID():
    return os.path.basename(os.getcwd())

def applyHook(template, hooks, newfile):
    """Apply hooks into the template file using insert_in_tag.py"""

def applyHooks(jc):
    """Apply hooks for JDL, JO, script."""
    jc.JobOptions.update('^#JO-HOOK')
    jc.Script.update('^#SCRIPT-HOOK')
    os.chmod(jc.Script.name(), 0744)

def listOfJobs(joblist_file='joblist'):
    output = open(joblist_file, 'r')
    jobs=[]
    for line in output.readlines():
        line = line[:-1]
        if line.startswith('#'): continue
        if len(line)>0: jobs.append(line)
    output.close()
    return jobs

def loopJobs(jc, joblist_file, funcForJob):
    """A"""
    jobs = listOfJobs(joblist_file)
    curdir=os.getcwd()
    for job in jobs:
        os.chdir(job)
        funcForJob(jc)
        os.chdir(curdir)
    
def prepareJob(jc):
    # expects input files in jobinfo file
    jobid = jobID()
    print 'Preparing job for %s using jobinfo.py' % jobid
    applyHooks(jc)
    if jc.JobType.name() == 'LXBATCH':
        workdir2 = jc.LxbatchWorkDir.name()
        curdir = os.getcwd()
        if curdir == workdir2:
            print 'prepareJobs should be called from (work_dir): %s' % \
                  jc.WorkDir.name()
            return
        jobdir2 = '%s/%s' % (workdir2, jobid)
        if not os.path.isdir(jobdir2):
            os.system('mkdir -p %s' % jobdir2)
        os.system('cp * %s' % jobdir2)
        os.chdir(curdir)
    return

def runJob(jc):
    """A"""
    out, err = 'runjob.out', 'runjob.err'
    jobid_out = 'jobid'
    jobid = jobID()
    print 'Submitting job %s' % jobid
    command = 'athena.py %s 1>>%s 2>>%s' % (jc.JobOptions.name(), out, err)
    (status, output) = tklog.system(command, altlog)

def statusJob(jc):
    """A"""
    out, err = 'statusjob.out', 'statusjob.err'
    jobid_out = 'jobid'
    command = 'bjobs'
    (status, output) = tklog.system(command, altlog)
    sys.stdout.write(output)
    sys.stdout.flush()
    
def getJob(jc):
    """Get the job output. Nothing to do for local/lxbatch jobs. In case of
    lxbatch jobs, the output should be copied to castor inside the job"""

def prepareJobs(jc, joblist_file):
    """Loop over a list of jobs and prepare input files for each job"""
    if jc.JobType.name() == 'LXBATCH':
        workdir2 = jc.LxbatchWorkDir.name()
        if workdir2 == '':
            print 'lxbatch_work_dir is empty'
            return
        if os.getcwd() == workdir2:
            print 'prepareJobs should be called from (work_dir): %s' % \
                  jc.WorkDir.name()
            return
        if os.path.isdir(workdir2): os.system('mkdir -p %s' % workdir2)
    os.system('cp jobconf.txt %s' % jc.LxbatchWorkDir.name())
    loopJobs(jc, joblist_file, prepareJob)
def runJobs(jc, joblist_file):
    """Loop over a list of jobs and run each of them"""
    loopJobs(jc, joblist_file, runJob)
def statusJobs(jc, joblist_file):
    """Loop over a list of jobs and query the status of each job"""
    loopJobs(jc, joblist_file, statusJob)
def getJobs(jc, joblist_file):
    """Loop over a list of jobs and retrieve the output of each job"""
    loopJobs(jc, joblist_file, getJob)


def runLocal(jc):
    opt = ''
    command = 'athena.py %s %s' % (opt, jc.JobOptions.filename())
    os.system(command)
    
if __name__=='__main__':
    pass

