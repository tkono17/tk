#!/usr/bin/env python
#-----------------------------------------------------------------
# K Job
#-----------------------------------------------------------------
class Conf:
    def __init__(self):
        self.ConfDir = ''
        self.OutDir = ''
        self.SentDir = ''
        self.InDir = ''
        self.DoneDir = ''
        self.LogDir = ''
    def confDir(self):

class Job:
    def __init__(self):
        self.name=""
        self.id=0
        self.queue = ''
        self.hostName=''
        self.submitDate=None
        self.doneDate=None
        self.status=''
    def print(self):
        print self.name
        print self.id

class Mgr:
    def __init__(self):
        self.topDir = []
        self.hostName = ''
        self.submitmgr = SubmitMgr()
        self.getmgr = GetMgr()
    def submit(self, job):
        print 'Submitting job ...'
        job_status = submitmgr.run()
    def get(self, job):
        print 'Getting job ...'
        getmgr.run()
        Job job = None;
        return job
    def purge(self, job):
        print 'Purging job ...'
    def kill(self, job):
        print 'Killing job ...'
    def run(self):

class SubmitMgr(Mgr):
    def __init__(self):
        print 'Submitter'
    def run(self):
        print 'Submitting job'

class GetMgr(Mgr):
    def __init__(self):
        print 'GetMgr'
    def run(self):
        print 'Getting job'

class ListMgr(Mgr):
    def __init__(self):
        print 'ListMgr'
    def run(self):
        print 'List jobs in the queue'
        
