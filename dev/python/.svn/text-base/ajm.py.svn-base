#!/usr/bin/env python

import os, sys
import re
import subprocess
from subprocess import PIPE
import commands
import optparse
import datetime

pbook_setup=os.path.join(os.environ['HOME'], 'setup_panda.sh')
dq2_setup_cmd='ini dq2'

cmd_pbook='/afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/0.3.10/bin/pbook'
def start_pbook():
    print 'Call pbook'
    p = subprocess.Popen([cmd_pbook], 
                         stdin=PIPE, stdout=PIPE, stderr=PIPE)
    ch_in, ch_out, ch_err = (p.stdin, p.stdout, p.stderr)

    print 'Communicate'
    #(outdata, errdata) = p.communicate('show(822)')
    #(outdata, errdata) = p._communicate_with_poll('')
    print 'OUT: ', os.read(p.stdout.fileno(), 1024)
    print 'ERR: ', os.read(p.stderr.fileno(), 1024)
    print 'go'
    print 'go2'
    p.stdin.write('show(822)\n')
    print 'Checkout'
    n = 0
    while n<10:
        tmp = os.read(p.stdout.fileno(), 1024)
        print 'OUT: ', tmp
        print 'N eol: %d /%d' % (tmp.count(os.linesep), len(tmp))
        n += 1
    print 'over'

def parse_response(f):
    lines = []
    try:
        i = 0
        while i < 100:
            print 'Reading ...'
            tmp = f.next()
            print 'Done next'
            lines.append(tmp)
            i += 1
    except StopIteration:
        print 'StopIteration exceptions'
        pass
    except:
        print 'Any exceptions'
    return lines

class JobStatus:
    kUNDEFINED = 'UNDEFINED'
    kDEFINED = 'DEFINED'
    kSUBMITTED = 'SUBMITTED'
    kNOT_SUBMITTED = 'NOT_SUBMITTED'
    kFINISHED = 'FINISHED'
    kFAILED = 'FAILED'
    kCANCELLED = 'CANCELLED'
    kCOPYING = 'COPYING'
    kCOPIED = 'COPIED'
    kDONE = 'DONE'
    kTO_BE_RESUBMITTED = 'TO_BE_RESUBMITTED'
    kRESUBMITTED = 'RESUBMITTED'
    
class Job:
    def __init__(self, name):
        words = name.split('/')
        self.name, self.name2 = '', ''
        if len(words) > 0: self.name = words[0]
        if len(words) > 1: self.name2 = words[1]
        self.jobsetID = -1
        self.jobID = -1
        self.workdir = ''
        self.status = JobStatus.kDEFINED
        self.n_subjobs = 0
        self.subjob_stats = {
            'activated': 0, 
            'running': 0, 
            'finished': 0, 
            'failed': 0, 
            'cancelled': 0, 
            }
        self.retryJobs = []
        self.subjobs = []
        self.resubmitJobs = []
        self.outDS = ''
        pass
    def getName(self):
        name = self.name
        if self.name2 != '': name = '%s/%s' % (self.name, self.name2)
        return name
    def subjobMap(self):
        x = {}
        for j in self.subjobs:
            x[j.JobID] = j
        return x
    def nJobsWithStatus(self, status, use_resubmitted=False):
        n_activated = self.subjob_stats['activated']
        n_running = self.subjob_stats['running']
        n_finished = self.subjob_stats['finished']
        n_cancelled = self.subjob_stats['cancelled']
        n_failed = self.subjob_stats['failed']
        for j in self.retryJobs:
            n_activated += j.nJobsWithStatus('activated')
            n_running += j.nJobsWithStatus('running')
            n_finished += j.nJobsWithStatus('finished')
            n_cancelled += j.nJobsWithStatus('cancelled')
            n_failed += j.nJobsWithStatus('failed')
        if use_resubmitted:
            if len(self.resubmitJobs)>0:
                n_failed = 0
                n_cancelled = 0
            for j in self.resubmitJobs:
                # active/running should be 0 in the parent job
                n_activated += j.nJobsWithStatus('activated')
                n_running += j.nJobsWithStatus('running')
                # Resubmib jobs only run on cancelled and failed parent jobs
                n_finished += j.nJobsWithStatus('finished')
                n_cancelled += j.nJobsWithStatus('cancelled')
                n_failed = j.nJobsWithStatus('failed')
        if status == 'activated': return n_activated
        elif status == 'running': return n_running
        elif status == 'finished': return n_finished
        elif status == 'failed': return n_failed
        elif status == 'cancelled': return n_cancelled
        else:
            return 0
        
    def isRunning(self):
        if self.nJobsWithStatus('running') != 0: return True
        else: return False
    def isDone(self):
        n = self.nJobsWithStatus('finished') + \
            self.nJobsWithStatus('failed') + \
            self.nJobsWithStatus('cancelled')
        if self.n_subjobs == n: return True
        else: return False
    def isFinished(self):
        return self.isDone() and self.finishedFraction()==1.0
    def hasCancelled(self):
        return self.nJobsWithStatus('cancelled') != 0
    def successRate(self, use_resubmitted=False):
        n1, n2, r = 0, 0, 0.0
        #
        n1 = self.nJobsWithStatus('finished', use_resubmitted)
        n2 = self.n_subjobs
        r = 0.0
        if n2 > 0: r = float(n1)/n2
        if use_resubmitted:
            n1 = 0
            n1 += self.nJobsWithStatus('finished', use_resubmitted)
            r = 0.0
            if n2 > 0: r = float(n1)/n2
        #print 'success rate = %4.2f (%d/%d)' % (r, n1, n2)
        return r
    def doneFraction(self, use_resubmitted=False):
        n0 = 0.0
        n1 = 0.0
        #
        n0 = self.n_subjobs
        n1 = self.nJobsWithStatus('finished') + \
             self.nJobsWithStatus('failed') + \
             self.nJobsWithStatus('cancelled')
        r = 0.0
        if n0 > 0: r = float(n1)/n0
        if not use_resubmitted or r != 1.0: return r
        if use_resubmitted:
            for j in self.resubmitJobs:
                n0 += j.n_subjobs
                n1 += j.nJobsWithStatus('finished') + \
                      j.nJobsWithStatus('failed') + \
                      j.nJobsWithStatus('cancelled')
        r = 0.0
        if n0 > 0: r = float(n1)/n0
        # print 'r = %4.2f (%d/%d)' % (r, n1, n0)
        return r
    def finishedFraction(self):
        n1 = self.nJobsWithStatus('finished')
        r = 0.0
        if self.n_subjobs > 0: r = float(n1)/(self.n_subjobs)
        return r
    def failedFraction(self):
        n1 = self.nJobsWithStatus('failed')
        r = 0.0
        if self.n_subjobs > 0: r = float(n1)/(self.n_subjobs)
        return r
    def badFraction(self):
        n1 = self.nJobsWithStatus('failed')
        n2 = self.nJobsWithStatus('cancelled')
        r = 0.0
        if self.n_subjobs > 0: r = float(n1+n2)/(self.n_subjobs)
        return r
    def update(self):
        pass
    def printIt(self):
        name = self.name
        if self.name2 != '': name = '%s/%s' % (self.name, self.name2)
        print 'Job'
        print '  Name (status): %s (%s)' % (name, self.status)
        print '  JobsetID: %d' % self.jobsetID
        print '  JobID: %d' % self.jobID
        print '  Working directory: %s' % self.workdir
        print '  Number of retryJobs: %d' % len(self.retryJobs)
        print '  Number of subjobs: %d' % len(self.subjobs)

class DSContainer:
    def __init__(self, name=''):
        self.name = name
        self.subContainers = []
        self.subDatasets = []
        
class JobMgr:
    def __init__(self, name=''):
        self.status = JobStatus.kUNDEFINED
        self.datasetListFile = ''
        self.jobs = []
        self.oldJobs = []
        self.datasetContainers = []
        self.name = name
        self.jobOptions = ''
        self.submitScripts = []
        
    def dump(self, filename):
        dumpObjs(self, filename)

    def save(self, filename):
        dumpObjs(self, filename)

    def load(self, filename):
        objs = loadObjs(filename)
        # print 'objs: ', objs
        if len(objs) == 1 and type(objs[0]) == type(JobMgr()):
            x = objs[0]
            self.status = x.status
            self.datasetListFile = x.datasetListFile
            self.jobs = x.jobs
            self.oldJobs = x.oldJobs
            self.datasetContainers = x.datasetContainers
            self.name = x.name
            self.jobOptions = x.jobOptions
            if hasattr(x, 'submitScripts'):
                self.submitScripts = x.submitScripts
        elif len(objs) == 3 and \
                 type(objs[1])==type([]) and type(objs[2]) == type([]):
            self.status = objs[0]
            self.datasetListFile = objs[1]
            self.jobs = objs[2]
            self.oldJobs = objs[3]
            self.datasetContainers = objs[4]

    def submit(self, dataset_file, dataset_aliases, pathena_opts):
        if os.path.exists(dataset_file):
            execfile(dataset_file)
            datasets = locals()['datasets']
            print datasets
        else:
            print 'Cannot find dataset definition file : %s' % dataset_file
        pass

    def addJob(self, job):
        """Add a new job. If there is a job with the same name already in the
        list, move the old one to oldJobs and replace it with the new one"""
        addJobs([job])
        pass
    def addJobs(self, jobs):
        """Add new jobs. If there is a job with the same name already in the
        list, move the old one to oldJobs and replace it with the new one"""
        jobs0 = self.jobs
        self.jobs = []
        new_names = []
        m = {}
        for j in jobs:
            m[j.name] = j
        new_names = map(lambda x: x.getName(), jobs)
        for j in jobs0: # copy existing jobs if not in the new list
            to_be_replaced = False
            if j.name in new_names:
                new_job = m[j.name]
                jid = new_job.jobsetID
                new_outDS = new_job.outDS
                if jid != -1 and j.jobsetID != jid:
                    # Resubmitted
                    jlist = map(lambda x: x.jobsetID, j.resubmitJobs)
                    if new_outDS == '':
                        print 'Cannot find the outDS for jobsetID=%d' % jid
                    elif j.outDS != new_outDS:
                        print 'DS changed: %s -> %s' % (j.outDS, new_outDS)
                        to_be_replaced = True
                    elif jid not in jlist:
                        j.resubmitJobs.append(new_job)
                    else:
                        # Already added to the resubmit jobs
                        pass
            if to_be_replaced:
                self.oldJobs.append(j)
            else:
                # Existing jobs (finished successfully or running)
                self.jobs.append(j)
                if j.name in new_names: new_names.remove(j.name)
        new_jobs = []
        for n in new_names:
            if n in m.keys(): new_jobs.append(m[n])
        # print 'Add %d new jobs' % len(new_jobs)
        self.jobs.extend(new_jobs)
    def addSubmitScript(self, x):
        self.submitScripts.append(x)
    def addDSContainer(self, x):
        self.datasetContainers.append(x)
    def findJob(self, jobsetid):
        for j in self.jobs:
            if j.jobsetID == jobsetid: return j
        return None
    def findJobByName(self, name):
        for j in self.jobs:
            if j.name == name: return j
        return None
    def allJobNames(self):
        return map(lambda x: x.name, self.jobs)
    def allDatasets(self):
        return []
    def allDatasetContainers(self):
        return []
    def datasetsFromJob(self):
        return []
    def jobDSMap(self):
        m = {}
        for j in self.jobs:
            if j.isDone() and j.finishedFraction()==1.0:
                m[j.getName()] = j.outDS
        return m
    def retryJobsetIDs(self, max_bad_fraction=0.8):
        """Retry failed jobs if the bad fraction was less than specified"""
        ids = []
        for j in self.jobs:
            if not j.hasCancelled() and j.isDone() and \
                   j.finishedFraction()<1.0 and \
                   j.status != JobStatus.kTO_BE_RESUBMITTED:
                r = j.badFraction()
                if r < max_bad_fraction:
                    jsid = j.jobsetID
                    if len(j.retryJobs) > 0: jsid = j.retryJobs[-1].jobsetID
                    ids.append(jsid)
        return ids
    def resubmitJobs(self, min_bad_fraction=0.5):
        """Resubmit failed jobs to a different site if the
        bad fraction was more than specified. Return job names"""
        v = []
        for j in self.jobs:
            #if j.status == JobStatus.kTO_BE_RESUBMITTED: continue
            if j.hasCancelled() or j.jobsetID == -1:
                v.append(j)
            elif j.isDone() and j.finishedFraction() < 1.0:
                r = j.badFraction()
                if r > min_bad_fraction or j.hasCancelled() or \
                   len(j.retryJobs) >= 3:
                    v.append(j)
        return v
    def resubmitJobsetIDs(self, min_bad_fraction=0.5):
        """Resubmit failed jobs to a different site if the
        bad fraction was more than specified"""
        return map(lambda x: x.jobsetID, self.resubmitJobs(min_bad_fraction))
    def resubmitJobNames(self, min_bad_fraction=0.5):
        """Resubmit failed jobs to a different site if the
        bad fraction was more than specified. Return job names"""
        return map(lambda x: x.name, self.resubmitJobs(min_bad_fraction))
    def printDetails(self):
        def printJobInfo(j, prefix=''):
            print '%sJobsetID: %d %s (%d/%d)' % \
                  (prefix, j.jobsetID, j.status,
                   j.nJobsWithStatus('finished'), j.n_subjobs)
        def printDetails(j):
            print '#--- Job %s (%d/%d)' % \
                  (j.name, j.nJobsWithStatus('finished', True), j.n_subjobs)
            print '       outDS=%s' % (j.outDS)
            status = j.status
            if j.isDone():
                j.status = 'DONE'
                if j.successRate() == 1.0:
                    j.status = JobStatus.kFINISHED
            printJobInfo(j, '       ')
            for j2 in j.resubmitJobs:
                printJobInfo(j2, '       ')
        for j in self.jobs:
            printDetails(j)
        return
    def printSummary(self):
        n100, n80, n50, n0 = 0, 0, 0, 0
        n_ok, m80, m50, m0 = 0, 0, 0, 0
        for j in self.jobs:
            r = j.doneFraction(True)
            if r == 1.0:
                n100 += 1
                sr = j.successRate(True)
                if sr == 1.0: n_ok += 1
                elif sr > 0.8: m80 += 1
                elif sr > 0.5: m50 += 1
                else: m0 += 1
            elif r > 0.8: n80 += 1
            elif r > 0.5: n50 += 1
            else: n0 += 1
        print '#--------------------------------------------------------'
        print '# JobMgr summary'
        print '#----------------'
        print '# Name: %s' % self.name
        print '# JobOptions: %s' % self.jobOptions
        print '# DatasetListFile: %s' % self.datasetListFile
        print '# No. of submit scripts  : %d' % len(self.submitScripts)
        print '# No. of jobs            : %d' % len(self.jobs)
        print '# No. of jobs resubmitted: %d' % len(self.oldJobs)
        n1 = len(self.datasetContainers)
        n2 = sum(map(lambda x: len(x.subContainers), self.datasetContainers))
        print '# No. of DS containers   : %d, Noutput=%d' % (n1, n2)
        print '# '
        print '# Progress of jobs'
        print '#   (100%% | >80%% | >50%% |  >0%% : %4d|%4d|%4d|%4d)' % \
              (n100, n80, n50, n0)
        print '# Success rate for finished jobs'
        print '#   (100%% | >80%% | >50%% |  >0%% : %4d|%4d|%4d|%4d)' % \
              (n_ok, m80, m50, m0)
        print '# %d jobs finished successfully' % n_ok
        print '#--------------------------------------------------------'

#----------------------------------------------------------------------
# Pickles
#----------------------------------------------------------------------
import cPickle

def dumpObjs(objs, fname):
    f = open(fname, 'wb')
    if type(objs) == type([]):
        for j in objs:
            cPickle.dump(j, f)
    else:
        cPickle.dump(objs, f)
    f.close()
    
def loadObjs(fname):
    f = open(fname, 'rb')
    objs = []
    try:
        while True:
            obj = cPickle.load(f)
            if obj != None:
                objs.append(obj)
    except EOFError:
        pass
    f.close()
    return objs
    
#----------------------------------------------------------------------
# 1. GRL -> Datasets
#----------------------------------------------------------------------
# Use atl_grl_ds.py

#----------------------------------------------------------------------
# 2. JO, Datasets -> Grid jobs
#----------------------------------------------------------------------
# Use panda_submit2.sh
# Need a tool to parse the result of pathena and save a pickle file
# - Name/Name2
# - List of grid jobs
#   - Jobset ID of a grid job (container dataaset)
#   - Number of jobs (simple dataset)
#   - Number of subjobs (files in a dataset)
#   - Status (SUBMITTED/NOT_SUBMITTED)
#   - Working directory

def parse_submission_log(logfile):
    import ajm
    jobs = []
    if os.path.exists(logfile):
        f = open(logfile, 'r')
        cur_job = []
        re1 = re.compile('Submitting pathena job ([\w._-]+)')
        re2 = re.compile('Successfully submitted pathena job')
        re3 = re.compile('JobsetID  : (\d+)')
        re4 = re.compile('SUBMITTED: ([\S]+)')
        for line in f.readlines():
            if len(line) > 0: line = line[:-1]
            mg1 = re1.search(line)
            if mg1:
                cur_job = ajm.Job(mg1.group(1))
                continue
            mg2 = re2.search(line)
            if mg2:
                mg3 = re3.search(line)
                if mg3: cur_job.jobsetID = int(mg3.group(1))
                continue
            mg4 = re4.search(line)
            if mg4:
                cur_job.workdir = mg4.group(1)
                cur_job.status = JobStatus.kSUBMITTED
                jobs.append(cur_job)
                continue
            pass
    else:
        print 'Logfile: %s does not exist' % logfile
    return jobs

def parse_jobsub(jobsub_out, jobsub_err):
    if os.path.exists(jobsub_out) and os.path.exists(jobsub_err):
        fout = open(jobsub_out, 'r')
        ferr = open(jobsub_err, 'r')
        re0 = re.compile('Executing pathena ... from directory ([\w_/.-]+)')
        re1 = re.compile('JobsetID  : (\d+)')
        re2 = re.compile('JobID  : (\d+)')
        re3 = re.compile('> run')
        re4 = re.compile('PandaID=(\d+)-(\d+)')

        dir = ''
        jobs = [] # List of [Jobset ID, JobID, Nsubjobs]
        
        out_lines = f.readlines()
        n = len(out_lines)
        i = 0
        while i < n:
            line = out_lines[i][:-1]
            # Check for working directory name
            mg = re0.search(line)
            if mg: dir = mg.group(1)
            else:
                # Check for job info
                mg = re1.search(line)
                if mg:
                    jobset_id, job_id, id1, id2 = 0, 0, 0, 0
                    jobset_id = int(mg.group(1))
                    mg = re2.search(out_lines[i+1])
                    if mg: job_id = int(mg.group(1))
                    mg = re4.search(out_lines[i+6])
                    if mg: id1, id2 = mg.group(1), mg.group(2)
                    jobs.append([jobset_id, job_id, id2-id1+1])
                    i += 6
            i += 1
                
    else:
        print "jobsub output files don't exist (%s, %s)" % \
              (jobsub_out, jobsub_err)
    pass
    

#----------------------------------------------------------------------
# 3. pbook related stuffs
#----------------------------------------------------------------------
# 3.1 Grid jobs -> Grid jobs (resubmit)
# 3.2 Grid jobs -> D-cache
#----------------------------------------------------------------------
def updateJobStatus(jobmgr, pbookCore):
    pjobs = pbookCore.getLocalJobList()
    pjmap = {}
    panda_status = (
        'activated', 
        'running',
        'failed',
        'finished',
        'cancelled',
        )
    def fillstats(j, pj, pjmap=None):
        words = pj.jobStatus.split(',')

        j.n_subjobs = 0
        j.subjob_stats['activated'] = 0
        j.subjob_stats['running'] = 0
        j.subjob_stats['finished'] = 0
        j.subjob_stats['failed'] = 0
        j.subjob_stats['cancelled'] = 0

        nsites = len(j.subjobs)
        for j2 in j.subjobs:
            #print 'Check subjob %d' % j2.jobID
            pj2 = pj.JobMap['%d' % j2.jobID]
            buildStatus = pj2.buildStatus
            #print 'build status: %s' % buildStatus
            words = pj2.jobStatus.split(',')[1:] # exclude build job
            j.n_subjobs += len(words)
            j.subjob_stats['activated'] += words.count('activated')
            j.subjob_stats['running'] += words.count('running')
            j.subjob_stats['finished'] += words.count('finished')
            j.subjob_stats['failed'] += words.count('failed')
            j.subjob_stats['cancelled'] += words.count('cancelled')

        n_done = j.subjob_stats['finished'] + j.subjob_stats['failed'] + \
                 j.subjob_stats['cancelled']
        n_success = j.subjob_stats['finished']
        if n_done == j.n_subjobs:
            j.status = JobStatus.kDONE
        #print 'n_success == self.n_subjobs: %d/%d' % (n_success, j.n_subjobs)
        if n_success == j.n_subjobs:
            #print ' ok'
            j.status = JobStatus.kFINISHED
##         j.n_subjobs = len(words)
##         j.subjob_stats['activated'] = words.count('activated')
##         j.subjob_stats['running'] = words.count('running')
##         j.subjob_stats['finished'] = words.count('finished')
##         j.subjob_stats['failed'] = words.count('failed')
##         j.subjob_stats['cancelled'] = words.count('cancelled')
        j.outDS = pj.outDS

    import ajm
    for j in pjobs:
        pjmap[int(j.JobsetID)] = j
    for j in jobmgr.jobs:
        if j.status == JobStatus.kNOT_SUBMITTED: continue
        jobsetid = j.jobsetID
        if jobsetid not in pjmap.keys(): continue
        pj = pjmap[jobsetid]
        
        j.subjobs = []
        for jid, tmp in pj.JobMap.iteritems():
            tmp2 = ajm.Job('%s/%s' % (j.name, jid))
            tmp2.jobID = int(jid)
            j.subjobs.append(tmp2)
            #fillstats(tmp2, tmp)
        fillstats(j, pj, pjmap)

        # If the job is finished but not successfully, check retry jobs
        retry_id = pj.retrySetID
        while retry_id != '':
            retry_id = int(retry_id)
            retry_job = pjmap[retry_id]
            tmp = filter(lambda x: x.jobsetID==retry_id, j.retryJobs)
            if len(tmp) == 0:
                subjob = ajm.Job(j.getName())
                subjob.name2 = '%d' % retry_id
                subjob.status = JobStatus.kSUBMITTED
                j.retryJobs.append(subjob)
            else:
                subjob = tmp[0]
            subjob.jobsetID = retry_id
            fillstats(subjob, retry_job)
            retry_id = retry_job.retrySetID
        if j.isDone() and j.finishedFraction() == 1.0:
            j.status = JobStatus.kFINISHED

        for j2 in j.resubmitJobs:
            pj2 = None
            if j2.jobsetID in pjmap.keys():
                j2.subjobs = []
                pj2 = pjmap[j2.jobsetID]
                for jid, tmp in pj2.JobMap.iteritems():
                    tmp2 = ajm.Job('%s/%s' % (j2.name, jid))
                    tmp2.jobID = int(jid)
                    j2.subjobs.append(tmp2)
                fillstats(j2, pj2, pjmap)


# DQ2 related stuffs
def findSitesForDS(dataset):
    cmd = 'dq2-ls -r %s' % dataset
    output = commands.getoutput(cmd)
    read_ds = False
    sites = []
    for line in output.split(os.linesep):
        if line.find('INCOMPLETE')>=0:
            read_ds = False
            continue
        elif line.find('COMPLETE:')>=0:
            read_ds = True
            words = line[9:].split(',')
            for w in words:
                sites.append(w.strip())
            break
##         if read_ds:
##             if line == 'None' or line.strip() == '':
##                 pass
##             else:
##                 sites.append(line.strip())
    return sites

def datasetsInContainer(dataset_container):
    cmd = 'dq2-list-datasets-container %s' % dataset_container
    status, output = commands.getstatusoutput(cmd)
    datasets = []
    if status == 0:
        for line in output.split(os.linesep):
            datasets.append(line)
    return datasets

#----------------------------------------------------------------------
# 5. D-cache -> file list
#----------------------------------------------------------------------
# Use mk_filelist.py

def datasetListLocation(dataset_list_file):
    dslists=[]
    grl_dir = os.path.dirname(dataset_list_file)
    f = open(dataset_list_file, 'r')
    for line in f.readlines():
        if len(line)>0 and line[-1]==os.linesep: line = line[:-1]
        line.strip()
        if len(line)>0 and line[0]!='#': dslists.append(line)
    return (grl_dir, dslists)

def findDSlistFile(jobname, dataset_list_files):
    ds_file, ds = '', ''
    for x in dataset_list_files:
        if os.path.exists(x):
            f = open(x, 'r')
            for line in f.readlines():
                if len(line) > 0: line = line[:-1].strip()
                if len(line)==0 or line[0] == '#': continue
                if ds_file != '': # order is important
                    ds = line.strip().strip('"\'')
                    break
                if line.find(jobname) >= 0: # order is important
                    ds_file = x
            f.close()
        else:
            print 'Cannot find dataset list file %s' % x
        if ds_file != '' and ds != '': break
    return (ds_file, ds)

def registerContainerAndDatasets(cont):
    cmd = 'dq2-register-container %s' % cont.name
    status, output = commands.getstatusoutput(cmd)
    if status != 0:
        print output
        cont.subDatasets = []
        return
    else:
        print 'Register container dataset: %s' % cont.name
        print output
    n = 0
    v = []
    for x in cont.subDatasets:
        cmd = 'dq2-register-datasets-container %s %s' % (cont.name, x)
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            print 'Error while registering dataset to a container'
            print output
            continue
        else:
            print 'Registered dataset to the container'
            print output
            v.append(x)
            n += 1
    ok = False
    if len(v) == len(cont.subDatasets):
        ok = True
    elif len(v) < len(cont.subDatasets):
        cont.subDatasets = v
    print 'Dataset container %s created with %d datasets (%d containers)' % \
          (cont.name, n, len(cont.subContainers))
    return ok
        

#----------------------------------------------------------------------
# Main functions
#----------------------------------------------------------------------
def check_env(progs):
    ok = True
    for p in progs:
        status, output = commands.getstatusoutput('which %s' % p)
        if status != 0:
            ok = False
            break
    # print 'check_env %s : %s' % (str(ok), str(progs))
    return ok

def main_addJobs(jobmgr, pickle_file, logfile):
    if not check_env([]): return

    if os.path.exists(pickle_file):
        jobmgr.load(pickle_file)

    #jobmgr.datasetListFile = datasetListFile
    jobs = parse_submission_log(logfile)
    jobmgr.addJobs(jobs)
    # print '%d jobs' % len(jobs)
    jobmgr.save(pickle_file)

def main_updateJobStatus(jm, pickle_file):
    if not check_env(['pbook']): return
    s = """import ajm
jm = ajm.JobMgr()
jm.load('%s')
ajm.updateJobStatus(jm, pbookCore)
jm.save('%s')
""" % (pickle_file, pickle_file)
    t = datetime.datetime.now()
    fname = 'ujs_%s.py' % t.strftime('%Y%m%d-%H%M%S')
    f = open(fname, 'w')
    f.write(s)
    f.close()
    os.system('pbook < %s' % fname)
    os.remove(fname)
    jm.load(pickle_file)
    
def main_retry(jm, pickle_file):
    if not check_env(['pbook']): return
    v = jm.retryJobsetIDs()
    t = datetime.datetime.now()
    fname = 'ujs_%s.py' % t.strftime('%Y%m%d-%H%M%S')
    f = open(fname, 'w')
    print '%d jobs to retry' % len(v)
    for x in v:
        print '  Retry(%d)' % x
        f.write('retry(%d)\n' % x)
    f.close()
    os.system('pbook < %s' % fname)
    os.remove(fname)
    main_updateJobStatus(jm, pickle_file)

def main_prepareResubmit(jm, pickle_file):
    if not check_env(['dq2-ls']): return
    print ' ==> Prepare resubmit'
    
    favorite_sites = (
        'DESY-HH', 'DESY-ZN',
        'TOKYO',
        'BNL', 
        )
    preferred_cloud = 'DE'

    grl_dir, dslists = datasetListLocation(jm.datasetListFile)
    dslists = map(lambda x: os.path.join(grl_dir, x), dslists)

    # script = 'resubmit_script.sh'
    jobs = jm.resubmitJobs()
    if len(jobs) == 0:
        print 'No jobs to resubmit'
        return
    script = '%s_resubmit%d.sh' % (jm.name, len(jm.submitScripts))
    fscript = open(script, 'w')
    fscript.write('#!/usr/bin/env zsh\n\n')
    fscript.write('jo=%s\n' % jm.jobOptions)
    
    re1 = re.compile('\.v(\d+)$')
    re2 = re.compile('\.v(\d+)/$')
    re_jn = re.compile('user\.tkohno\.data\.([^\.]+)\.')
    fscript.write('if [[ -e panda_submit.log ]]; then'+os.linesep)
    fscript.write('  rm panda_submit.log'+os.linesep)
    fscript.write('fi'+os.linesep)
    for job in jobs:
        job_name = job.name
        (ds_file, inDS) = findDSlistFile(job_name, dslists)
        print '%s => %s' % (job_name, inDS)

        jn = jm.name
        site, cloud = '', ''
        v = findSitesForDS(inDS)
        #print 'Possible sites: ', v
        site=''
        ok=False
        for x in favorite_sites:
            if ok: break
            for ss in v:
                #print 'Checking site %s' % ss
                if re.search('(%s.*_DATADISK)' % x, ss) != None:
                    site = x
                    ok = True
                    break
                elif re.search('(%s.*_MCDISK)' % x, ss) != None:
                    site = x
                    ok = True
                    break
        if site == '':
            print ' --> No match to favorite site, submit to cloud %s' % \
                  preferred_cloud
            cloud = preferred_cloud
        site, cloud = '', ''
        s = 'panda_submit2.sh -d %s -k %s -n 2 -j $jo -s "%s" --append-log' % \
            (ds_file, job_name, site)
        s += ' --destSE DESY-HH_LOCALGROUPDISK'
        if cloud != "": s += ' -c %s' % cloud
        if jn != '': s += ' --jobName %s' % jn
        ver = 0
        print job.outDS
        mg1 = re1.search(job.outDS)
        mg2 = re2.search(job.outDS)
        if mg1: ver = int(mg1.group(1)) # + 1
        if mg2: ver = int(mg2.group(1)) # + 1
        s += ' -v v%d' % ver
        fscript.write(s+os.linesep)
        job.status = JobStatus.kTO_BE_RESUBMITTED
    fscript.close()
    jm.addSubmitScript(os.path.abspath(script))
    os.system('chmod +x %s' % script)
    jm.save(pickle_file)
    print 'Run the script %s to resubmit jobs' % script

def main_prepareDaTRI(jm, pickle_file):
    if not check_env(['dq2-ls']): return
    print ' ==> Prepare for data transfer using DaTRI'

    dsc_prefix = 'user.tkohno.dsc'
    v = [] # datasets already assigned to a container
    for x in jm.datasetContainers:
        v.extend(x.subContainers)
    n = len(jm.datasetContainers)
    import ajm
    cont = ajm.DSContainer('%s.%s_%d/' % (dsc_prefix, jm.name, n))
    for j in jm.jobs:
        if j.isFinished() and j.outDS not in v:
            cont.subContainers.append(j.outDS)
            cont.subDatasets.extend(datasetsInContainer(j.outDS))
    n = len(cont.subContainers)
    if n > 0:
        print 'Create DS container from %d containers' % n
        if registerContainerAndDatasets(cont):
            jm.addDSContainer(cont)
        elif len(cont.subDatasets)>0:
            print 'Warning: some datasets were not registered to the container'
            jm.addDSContainer(cont)
        else:
            print 'Could not register DS container %s' % cont.name
        jm.save(pickle_file)
    else:
        print 'DS container has %d dataset containers' % n

def main_updateDaTRI(pickle_file):
    if not check_env(['']): return
    print 'Not implemented yet, check the status on panda monitor'

def main_status(jm, pickle_file, no_action=False, do_datri=False):
    print 'Status before update'
    jm.printSummary()

    #----------------------------------------
    # Update job status
    #----------------------------------------
    main_updateJobStatus(jm, pickle_file)
    jm.printSummary()

    if not no_action:
        main_prepareResubmit(jm, pickle_file)
        main_retry(jm, pickle_file)
    
    #----------------------------------------
    # Job transfer
    #----------------------------------------
    if not no_action and do_datri:
        main_prepareDaTRI(jm, pickle_file)
    print 'Status after update'
    jm.printSummary()
    jm.save(pickle_file)

def main_outputSummary(jm, output_file):
    if not check_env(['dq2-ls', 'dcls']): return
    print 'Making output summary. This may take some time O(minutes)'

    finished_jobs = filter(lambda x: x.isFinished(), jm.jobs)
    (grl_dir, dslists) = datasetListLocation(jm.datasetListFile)
    dslists = map(lambda x: os.path.join(grl_dir, x), dslists)

    job_ds_map = {}
    dsfile_ds_map = {}
    dsfile_nall_map = {}
    dsfile_n_map = {}

    contlist = []
    for x in jm.datasetContainers:
        contlist.extend(x.subContainers)

    for j in jm.jobs:
        (ds_file, inDS) = findDSlistFile(j.name, dslists)
        dsfile_key = os.path.basename(ds_file).replace('.sh', '')

        if dsfile_key in dsfile_nall_map.keys():
            dsfile_nall_map[dsfile_key] += 1
        else:
            dsfile_nall_map[dsfile_key] = 1

        if not j.isFinished():
            if j.outDS in contlist:
                print 'Job %s included in the output DScontainer while still running' % j.name
            continue
        if j.outDS not in contlist:
            print '%s finished but not ready for transfer' % j.outDS
        
        all_datasets = datasetsInContainer(j.outDS) # time consuming!!!
        job_ds_map[j.name] = all_datasets
        if dsfile_key in dsfile_ds_map.keys():
            dsfile_ds_map[dsfile_key].extend(all_datasets)
            dsfile_n_map[dsfile_key] += 1
        else:
            dsfile_ds_map[dsfile_key] = list(all_datasets)
            dsfile_n_map[dsfile_key] = 1

    print 'Writing output datasets into file'
    keys1 = job_ds_map.keys()
    keys2 = dsfile_nall_map.keys()
    keys1.sort()
    keys2.sort()
    f = open(output_file, 'w')
    f.write('data_samples = {\n')
    f.write('\n# Per job\n')
    for k in keys1:
        f.write('    "%s": (\n' % k)
        for x in job_ds_map[k]:
            f.write('        "%s", \n' % x)
        f.write('    ),\n')
    f.write('\n# Per list of jobs as defined in file %s\n' % ds_file)
    for k in keys2:
        n = dsfile_nall_map[k]
        n1 = 0
        if k in dsfile_n_map.keys(): n1 = dsfile_n_map[k]

        f.write('    "%s": ( # (%d/%d)\n' % (k, n1, n))
        for x in dsfile_ds_map[k]:
            f.write('        "%s", \n' % x)
        f.write('    ), \n')
    f.write('}\n')
    f.close()
    
#----------------------------------------------------------------------
# Main program
#----------------------------------------------------------------------
def create_parser():
    parser = optparse.OptionParser()
    parser.add_option('-a', '--add-jobs', 
                      action='store', dest='jobsub_log', default='',
                      help='Update from job submission logfile (arg=logfile)')
    parser.add_option('--submit-pathena',
                      action='store_true', dest='submit_pathena', default=False,
                      help='Submit pathena job')
    parser.add_option('--dataset-file',
                      action='store', dest='dataset_file', default='',
                      help='Dataset definition file (dictionary of alias=>dataset)')
    parser.add_option('--dataset-aliases',
                      action='store', dest='dataset_aliases', default='',
                      help='Dataset aliases')
    parser.add_option('--pathena-options',
                      action='store', dest='pathena_options', default='',
                      help='pathena options')
    parser.add_option('--add-job',
                      action='store', dest='job_name_id', default='',
                      help='Add new job specifying <name>,<jobsetID>,<submitDir>,<DS>')
    parser.add_option('-s', '--show-summary',
                      action='store_true', dest='show_summary', default=False,
                      help='Show summary without making update')
    parser.add_option('--show-details',
                      action='store_true', dest='show_details', default=False,
                      help='Show details of the progress of all jobs')
    parser.add_option('-f', '--pickle_file',
                      action='store', dest='file', default='',
                      help='Pickle file name')
    parser.add_option('-u', '--update',
                      action='store_true', dest='update', default=False,
                      help='Update status of jobs')
    parser.add_option('-n', '--no-action',
                      action='store_true', dest='no_action', default=False,
                      help='Do not take any action (retry, resubmit, DaTRI)')
    parser.add_option('-d', '--dataset-summary',
                      action='store', dest='dataset_summary',
                      default='',
                      help='Generate the summary of output datasets to the file specified')
    parser.add_option('--set-name',
                      action='store', dest='set_name', default='',
                      help='Set job name')
    parser.add_option('--set-joboptions',
                      action='store', dest='set_joboptions', default='',
                      help='Set jobOptions file name')
    parser.add_option('--set-datasetlist',
                      action='store', dest='set_datasetlist', default='',
                      help='Set dataset list file')
    parser.add_option('--do_DaTRI',
                      action='store_true', dest='do_DaTRI', default=False,
                      help='Prepare DaTRI for finished jobs')
    return parser

if __name__ == '__main__':
    parser = create_parser()
    (options, args) = parser.parse_args()

    import ajm # Needed to have ajm. in the pickle file
    jobmgr = ajm.JobMgr()
    if options.file != '' and os.path.exists(options.file):
        print 'Loading job info from %s' % options.file
        jobmgr.load(options.file)

    setting_info=False
    if options.set_name != '':
        setting_info = True
        jobmgr.name = options.set_name
    if options.set_joboptions != '':
        setting_info = True
        jobmgr.jobOptions = os.path.abspath(options.set_joboptions)
    if options.set_datasetlist != '':
        setting_info = True
        jobmgr.datasetListFile = os.path.abspath(options.set_datasetlist)

    if setting_info and options.file != '': jobmgr.save(options.file)

    if not (os.path.exists(options.file) or options.jobsub_log != ''):
        parser.print_help()
        sys.exit(1)

    if options.submit_pathena:
        jobmgr.submit(options.dataset_file, options.dataset_aliases,
                      options.pathena_options)

    if os.path.exists(options.jobsub_log):
        main_status(jobmgr, options.file, True, False)
        main_addJobs(jobmgr, options.file, options.jobsub_log)
    elif options.jobsub_log != '':
        print 'Job submission log file %s does not exist' % options.jobsub_log
        parser.print_help()
        sys.exit(1)
    if options.job_name_id != '':           
        main_status(jobmgr, options.file, True, False)
        words = options.job_name_id.split(',')
        if len(words) == 3 or len(words) == 4:
            j = ajm.Job(words[0])
            j.jobsetID = int(words[1])
            j.workdir = words[2]
            if len(words)>3: j.outDS = words[3]
            j.status = JobStatus.kSUBMITTED
            jobmgr.addJobs([j])

    if options.dataset_summary != '':
        main_outputSummary(jobmgr, options.dataset_summary)
    if options.update:
        main_status(jobmgr, options.file, options.no_action, options.do_DaTRI)
    elif options.show_summary:
        jobmgr.printSummary()
    elif options.show_details:
        jobmgr.printDetails()
        
    if options.file != '':
        print 'Saving job info to %s' % options.file
        jobmgr.save(options.file)
    
