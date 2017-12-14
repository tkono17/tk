#!/usr/bin/env python

import os, sys
import re

def findJobs(pbookCore,
             dataset_pattern='', status='', status_not=''):
    jobs = pbookCore.getLocalJobList()
    out = []
    re0 = None
    if dataset_pattern != '': re0 = re.compile(dataset_pattern)
    for j in jobs:
        ok = True
        jobstatus = j.jobStatus.split(',')
        if re0:
            mg = re0.search(j.outDS)
            if not mg: ok = False
        if status != '':
            if jobstatus.count(status) == 0: ok = False
        if status_not != '':
            if jobstatus.count(status_not) > 0: ok = False
        if ok: out.append(j)
    return out

def getDSNames(pattern, pbookCore):
    re0 = re.compile(pattern)
    jobs = pbookCore.getLocalJobList()
    names = []
    for j in jobs:
        mg = re0.search(j.outDS)
        if mg and j.outDS not in names: names.append(j.outDS)
    return names

def getJobHistory(job_name, pbookCore):
    jobs = pbookCore.getLocalJobList()
    v = []
    for j in jobs:
        if j.outDS == job_name: v.append(j)
    v.sort(cmp=lambda x, y: x.JobsetID < y.JobsetID)
    return v

def statusString(job):
    words = job.jobStatus.split(',')
    keys = []
    x = ''
    for w in words:
        if w not in keys: keys.append(w)
    keys.sort()
    for k in keys:
        x += '%s(x%d)' % (k, words.count(k))
    return x

def dumpJobInfo(jobs):
    v = jobs
    if type(jobs) != type([]): v = [jobs]
    for x in v:
        print '%d %s %s' % (int(x.JobsetID), x.outDS, statusString(x))

def test(pbookCore):
    job_names = getDSNames('user.tkohno.*Jpsiee.*Npv15.*v1', pbookCore)
    print 'N jobs: %d' % len(job_names)
    for jn in job_names:
        v = getJobHistory(jn, pbookCore)
        s = ''
        for j in v:
            s += '%s %s, ' % (j.JobsetID, statusString(j))
        print '%-20s %s' % (jn, s)
        
