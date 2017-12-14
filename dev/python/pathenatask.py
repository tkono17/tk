#!/usr/bin/env python
#---------------------------------------------------------------------
# pathenatask.py
#---------------
# Package for pathena task
#---------------------------------------------------------------------
from taskmgr import *
import re
import string
import subprocess
import optparse

DSprefix = 'user.tkohno.data'

log = logging.getLogger('taskmgr.py') #.getChild('pathenatask.py') #python2.7

class AthenaTaskDefinition(TaskDefinition):
    def __init__(self, name, jo='', athenaRelease='', testarea='',
                 outputFiles=[]):
        TaskDefinition.__init__(self, name)
        self.jobOptionsFile = jo
        self.athenaRelease = athenaRelease
        self.testarea = testarea
        self.outputFiles = list(outputFiles)
        if self.athenaRelease == '':
            self.athenaRelease = '%s,%s' % (os.environ['AtlasProject'],
                                            os.environ['AtlasVersion'])
        if self.testarea == '':
            self.testarea = os.environ['TestArea']
        pass
    def releaseNumber(self):
        mg = re.search('(\d+)((?:\.\d+){2,4})', self.athenaRelease)
        if mg:
            return mg.group(0)
        else:
            return '0.0.0'
    def __str__(self):
        s = TaskDefinition.__str__(self)
        s += '  JobOptionsFile => %s\n' % self.jobOptionsFile
        s += '  AthenaRelease  => %s\n' % self.athenaRelease
        return s
    pass

class PathenaTaskDefinition(AthenaTaskDefinition):
    def __init__(self, name, jo, inDS,
                 athenaRelease='', testarea='', outputFiles=[],
                 outDS='', version='v1'):
        AthenaTaskDefinition.__init__(self, name, jo,
                                     athenaRelease, testarea, outputFiles)
        self.inDS = inDS
        self.outDS = outDS
        self.version = version
        pass
    def createOutDSName(self):
        global DSprefix
        jotype = os.path.basename(self.jobOptionsFile)
        jotype = jotype.lstrip('^test').rstrip('.py')
        rel = self.releaseNumber()
        inDS_name = self.inDS.rstrip('/')
        idc = inDS_name.find(':')
        if idc >= 0:
            inDS_name = inDS_name[idc+1:]
        ipos = -1
        for i in range(3):
            ipos = inDS_name.find('.', ipos+1)
        if ipos >= 0 and ipos < len(inDS_name): inDS_name = inDS_name[:ipos]
        return '%s.%s.%s.%s.%s' % \
               (DSprefix, jotype, inDS_name, rel, self.version)
    def __str__(self):
        s = AthenaTaskDefinition.__str__(self)
        s += '  inDS           => %s\n' % self.inDS
        s += '  outDS          => %s\n' % self.outDS
        s += '  version        => %s\n' % self.version
        return s
    pass

#---------------------------------------------------------------------
# Classes for grid job
#---------------------------------------------------------------------
class GridJob:
    def __init__(self, jobsetID, jobID, site='', buildStatus='',
                 NInputFiles=0, subjobs_status={}):
        self.jobsetID = jobsetID
        self.jobID = jobID
        self.site = site
        self.buildStatus = buildStatus
        self.NInputFiles = NInputFiles
        if len(subjobs_status) == 0:
            self.subjobs_status = {
                Status.kRunning: 0, 
                Status.kFinished: 0, 
                Status.kFailed: 0,
                Status.kCancelled: 0, 
                }
        else:
            self.subjobs_status = dict(subjobs_status)
        pass
    def updateStatus(self, pbook_status):
        words = pbook_status.split(',')
        if len(words) > 0: self.buildStatus = words[0]
        self.subjobs_status = words[1:]
    def status(self):
        if self.buildStatus == Status.kFailed:return Status.kCancelled
        elif self.subjobs_status[Status.kRunning]>0: return Status.kRunning
        elif self.subjobs_status[Status.kCancelled]>0: return Status.kCancelled
        elif self.subjobs_status[Status.kFailed]>0: return Status.kFailed
        elif self.subjobs_status[Status.kFinished]>0: return Status.kFinished
        else: return Status.kWaiting
    def __str__(self):
        s = '    Job (jobID=%d, site=%s, Nfiles=%s, status=%s)\n' % \
            (self.jobID, self.site, str(self.NInputFiles), self.status())
        return s
    pass

class GridJobSet:
    def __init__(self, jobsetid):
        self.jobsetID = jobsetid
        self.jobs = []
    def findJob(self, jobID):
        for j in self.jobs:
            if j.jobID == jobID: return j
        return None
    def addJob(self, job):
        for j in self.jobs:
            if j.jobID == job.jobID: return self
        self.jobs.append(job)
        return self
    def status(self):
        ret = Status.kWaiting
        prio_cancelled = (Status.kRunning,)
        prio_failed = (Status.kRunning, Status.kCancelled,)
        prio_finished = (Status.kRunning, Status.kCancelled, Status.kFailed,)
        for j in self.jobs:
            s = j.status()
            if s == Status.kRunning:
                ret = Status.kRunning
            elif s == Status.kCancelled and ret not in prio_cancelled:
                ret = Status.kCancelled
            elif s == Status.kFailed and ret not in prio_failed:
                ret = Status.kFailed
            elif s == Status.kFinished and ret not in prio_finished:
                ret = Status.kFinished
        return ret
    def __str__(self):
        s = '  JobSet (jobsetID=%d, status=%s)\n' % \
            (self.jobsetID, self.status())
        for x in self.jobs:
            s += str(x)
        return s
    pass

#---------------------------------------------------------------------
# Classes for the running task (input -> output)
#---------------------------------------------------------------------
class PathenaTask(Task):
    def __init__(self, job, pathena_opts={'--destSE': 'TOKYO-LCG2_LOCALGROUPDISK',
                                          '--nGBPerJob': 2,}):
        Task.__init__(self, job)
        self.NInputFiles = 0
        self.jobsets = [] # Jobs submitted by pathena or retry
        self.pathena_opts = dict(pathena_opts)
        self.taskID = -1
        # Temporary data
    def findJobSet(self, jobsetID):
        for j in self.jobsets:
            if j.jobsetID == jobsetID: return j
        return None

    def addJobSet(self, jobsetid, jobid, nfiles, site):
        js = self.findJobSet(jobsetid)
        if js == None:
            log.info('Adding GridJobSet: %d' % jobsetid)
            js = GridJobSet(jobsetid)
            self.jobsets.append(js)
        j = js.findJob(jobid)
        if j == None:
            log.info('Adding GridJob: %d to set %d' % (jobid, jobsetid))
            j = GridJob(jobsetid, jobid, site=site, NInputFiles=nfiles)
            js.addJob(j)
        else:
            #print 'Job %d/%d already exists' % (jobsetid, jobid)
            pass
        return self
    def prepare(self):
        log.debug('preparing ...')
        if self.taskDefinition.outDS == '':
            self.taskDefinition.outDS = self.taskDefinition.createOutDSName()
        if not os.environ.has_key('TestArea'):
            return False
        self.workdir = '%s/jobs/%s/run' % \
                       (os.environ['TestArea'], self.taskDefinition.name)
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)
        return Status.kPrepared
    def run(self):
##         self.pathena_opts = {
##                 '--destSE': 'DESY-HH_LOCALGROUPDISK',
##                 '--nGBPerJob': 6,
##                 }
#        self.taskDefinition.jobOptionsFile = self.taskDefinition.jobOptionsFile.replace('16.6.2.5', '16.6.3.5')
        self.action_run.cmd = 'pathena --inDS %s --outDS %s' % \
                              (self.taskDefinition.inDS,
                               self.taskDefinition.outDS)
        if self.pathena_opts.has_key('--destSE'):
            self.pathena_opts.pop('--destSE')
        for (k, v) in self.pathena_opts.iteritems():
            self.action_run.cmd += ' %s %s' % (k, v)
        self.action_run.cmd += ' %s' % self.taskDefinition.jobOptionsFile
        cwd = os.getcwd()
        os.chdir(self.workdir)
        out, err = self.execCmd(self.action_run.cmd)
        base, first = 'run', True
        if len(self.jobsets) > 0:
            first = False
            base = 'run%d' % len(self.jobsets)
        outname = '%s/%s.out' % (self.workdir, base)
        errname = '%s/%s.err' % (self.workdir, base)
        if first:
            self.action_run.out = outname
            self.action_run.err = errname
        else:
            if not hasattr(self.action_rerun, 'logs'):
                self.action_rerun.logs = []
            self.action_rerun.logs.append( (outname, errname))
        if not self.do_echo:
            self.saveToFile(outname, out)
            self.saveToFile(errname, err)
        os.chdir(cwd)
        # Parse output
        out, err = None, None
        state = self.parse_run(out, err) # adds the job info
        #return Status.kWaiting
        return state

    def parse_run(self, out=None, err=None):
        # Job info: job1=(site, nfiles, nsubjobs) (from err)
        #           job2=(jobsetid, jobid) (from out)
        jobs1, jobs2 = [], []
        self.taskID = -1
        n_allfiles = 0
        n_missing = -1
        outstate = Status.kPrepared

        (outfile, errfile) = (self.action_run.out, self.action_run.err)
        if len(self.action_rerun.logs)>0:
            log.debug('Parse from the last rerun logfile')
            outfile, errfile = self.action_rerun.logs[-1]
        if out == None:
            if os.path.exists(outfile):
                log.info('Reading run.out from %s' % outfile)
                f = open(outfile)
                out = string.join(f.readlines(), os.linesep)
                f.close()
        if err == None:
            if os.path.exists(errfile):
                log.info('Reading run.err from %s' % errfile)
                f = open(errfile)
                err = string.join(f.readlines(), os.linesep)
                f.close()

        if out == None or err == None:
            log.warning('stdout/stderr are null')
            log.warning('  outfile=%s' % str(outfile))
            log.warning('  errfile=%s' % str(errfile))
            return False

        # Parse stderr to retrieve jediTaskID
        jobsetid, jobid = -1, -1
        for line in err.split(os.linesep):
            # mg1 = re.search('JobsetID  : (\d+)', line)
            mg1 = re.search('jediTaskID=(\d+)', line)
            if mg1: self.taskID = int(mg1.group(1))
            # mg2 = re.search('JobID  : (\d+)', line)
            # if mg2: jobid = int(mg2.group(1))
            # if jobsetid > 0 and jobid > 0:
            #     jobs1.append( (jobsetid, jobid))
            #     jobsetid, jobid = -1, -1 # resetting

        # # Parse stderr
        # n_files, site, n_subjobs = 0, '', 0
        # done = False
        # for line in err.split(os.linesep):
        #     # Check missing files
        #     mg = re.search('(\d+) files are missing or unchecked at', line)
        #     if mg: n_missing = int(mg.group(1))
        #     # Info on submitted job
        #     mg1 = re.search('use (\d+) files', line)
        #     if mg1: n_files = int(mg1.group(1))

        #     mg2 = re.search('submit (\d+) subjobs to ([\S]+)$', line)
        #     if mg2:
        #         n_subjobs = int(mg2.group(1))
        #         site = mg2.group(2)

        #     mg = re.search('Done\. No jobs to be submitted since all', line)
        #     if mg: done = True
        #     if n_files>0 and site != '' and n_subjobs > 0:
        #         n_allfiles += n_files
        #         jobs2.append( (site, n_files, n_subjobs))
        #         n_files, site, n_subjobs = 0, '', 0
        #     # If all files are available, there's no missing file
        #     if re.search('all files are available at', line):
        #         m_missing = 0
        # if n_missing > 0: n_allfiles += n_missing
        # if done: outstate = Status.kFinished
        
        # if self.NInputFiles == 0:
        #     # The total number of files must be gathered for the first submit.
        #     # Resubmit might only run on a subset.
        #     self.NInputFiles = n_allfiles

        if self.taskID > 0:
            log.info('JediTaskID=%d' % self.taskID)
            outstate = Status.kWaiting
        # elif len(jobs1) != len(jobs2):
        #     log.warning('Number of jobs parsed from stdout and stderr differs')
        #     log.warning(' N(out),N(err) = %d,%d' % (len(jobs1), len(jobs2)))
        # elif len(jobs1) > 0:
        #     if not done: outstate = Status.kWaiting
        #     for i in range(len(jobs1)):
        #         j1 = jobs1[i]
        #         j2 = jobs2[i]
        #         log.info('Add jobset jobsetID=%d, jobID=%d' % (j1[0], j1[1]))
        #         self.addJobSet(j1[0], j1[1], j2[1], j2[0])
        else:
            log.warning('No jobset/job info found in the pathena out/err')
        return outstate
    
    def update(self):
        #if len(self.jobsets) == 0: return False
        # jobsetids = map(lambda x: x.jobsetID, self.jobsets)
        #s = '['
        #for x in jobsetids: s += '%d, ' % x
        #s += ']'
        s = '[%d]' % self.taskID
        p = launchPbookProcess()
        cmd = """from pathenatask import *
updateFromPbook(pbookCore, %s)
""" % (s) #, self.taskDefinition.outDS)
        (out, err) = p.communicate(cmd)
        log.debug('pbook-out: %s' % out)
        taskstatus = self.status
        for line in out.split(os.linesep):
            #print line
            i = line.find('JOB_STATUS=')
            i2 = line.find('CHILD_JOBS=')
            if i < 0 and i2 < 0: continue
            #
            if i2>=0:
                words = line[i2+len('CHILD_JOBS='):].split(',')
                words.sort()
                log.debug('Parsing CHILD_JOBS: ')
                re0 = re.compile('(\d+):(\d+):(\d+)')
                for w in words:
                    mg = re0.search(w)
                    if mg == None: continue
                    tid = int(mg.group(1))
                    jsid = int(mg.group(2))
                    jid = int(mg.group(3))
                    log.debug('CHILD_JOBS mg=%s' % str(mg))
                    log.debug('CHILD_JOBS IDs: %s' % (str(mg.groups()) ) )
                    nfiles = 0
                    site = '?'
                    self.addJobSet(jsid, jid, nfiles, site)
                    #print '%d %d %d %s' % (jsid, jid, nfiles, site)
            #
            if i >= 0:
                words = line[i+len('JOB_STATUS='):].split(',')
                tid, jobsetid, jobid = 0, 0, 0
                nfiles, site = 0, '?'
                build, run, fin, fai, can = '', 0, 0, 0, 0
                for w in words:
                    kv = w.split(':')
                    if len(kv) != 2: continue
                    k, v = kv[0], kv[1]
                    if k == 'taskID': tid = int(v)
                    elif k == 'jobsetID': jobsetid = int(v)
                    elif k == 'jobID': jobid = int(v)
                    elif k == 'build': build = v
                    elif k == 'defined': run += int(v)
                    elif k == 'running': run += int(v)
                    elif k == 'holding': run += int(v)
                    elif k == 'finished': fin = int(v)
                    elif k == 'failed': fai = int(v)
                    elif k == 'cancelled': can = int(v)
                    else: log.warning('Unrecognized key in job update %s' % k)
                #log.debug('job update: %d %d %s %d %d %d %d' % \
                #          (jobsetid, jobid, build, run,fin,fai,can))
                j = self.findJobSet(jobsetid)
                if j == None:
                    self.addJobSet(jobsetid, jobid, nfiles, site)
                    j = self.findJobSet(jobsetid)
                if j != None: j = j.findJob(jobid)
                if j != None:
                    j.subjobs_status = {
                        Status.kRunning: run, 
                        Status.kFinished: fin,
                        Status.kFailed: fai,
                        Status.kCancelled: can,
                        }
            pass
        if len(self.jobsets):
            taskstatus = self.jobsets[-1].status()
        else:
            log.debug('Number of subjobs for taskID=%d' % \
                          (self.taskID, len(jobsets)) )
        return taskstatus
    def rerun(self):
        """retry or resubmit"""
        self.run()
        return Status.kWaiting
    def __str__(self):
        s = Task.__str__(self)
        s += 'Jobsets (taskID=%d, NInputFiles=%d, x%d):\n' % \
            (self.taskID, self.NInputFiles, len(self.jobsets))
        for x in self.jobsets:
            s += str(x)
        return s
    def dump(self):
        pass
    def printSummary(self):
        Task.printSummary(self)
        pass
    def printDetails(self):
        pass
    pass

#---------------------------------------------------------------------
# DQ2 tools
#---------------------------------------------------------------------
class Dq2Interface:
    def __init__(self, nickname='tkohno',
                 dcache_localgroupdisk='/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk',
                 dcache_dataarea='/pnfs/desy.de/atlas/dq2/atlaslocalgroupdisk/user/tkohno/data',
                 dcap_header='dcap://dcache-atlas-dcap.desy.de:22125'):
        #dcap_header='dcap://dcache-ses-atlas.desy.de:22125'):
        self.nickname = nickname
        self.dcache_localgroupdisk = dcache_localgroupdisk
        self.dcache_dataarea = dcache_dataarea
        self.dcap_header = dcap_header
        pass
    def checkdq2(self):
        status = subprocess.call('which dq2-ls'.split())
        if status == 0: return True
        else:
            log.warning('dq2 commands not available')
            return False
    def getListOfFilesOnDcache(self, ptask, pat='', add_dcap_header=False):
        v = []
        datasets = self.getListOfDatasets(ptask.taskDefinition.outDS)
        for ds in datasets:
            dp = '%s/%s' % (self.dcache_dataarea, ds)
            cmd = 'dcls %s' % dp
            p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode == 0:
                for x in out.split(os.linesep):
                    if pat == '' or re.search(pat, x):
                        v.append('%s/%s' % (dp, x))
        if add_dcap_header:
            v = map(lambda x: '%s%s' % (self.dcap_header, x), v)
        return v
    def numberOfFilesInDataset(self, ds, pat=''):
        n = 0
        cmd = 'dq2-list-files %s' % ds
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0:
            for x in out.split(os.linesep):
                if pat == '' or re.search(pat, x):
                    n += 1
        return n
    def getListOfDatasets(self, ds_container):
        v = []
        if not self.checkdq2(): return v
        if not ds_container.endswith('/'): ds_container += '/'
        cmd = 'dq2-list-datasets-container %s' % ds_container
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0:
            v = filter(lambda x: x.startswith(ds_container[:3]),
                       out.split(os.linesep))
        else:
            log.warning('Error while checking datasets in the container')
            log.warning(' cmd=%s' % cmd)
        return v
#---------------------------------------------------------------------
# Functions for interacting with pbook
#---------------------------------------------------------------------
def launchPbookProcess():
    p = subprocess.Popen('pbook', stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p

def findJobset(pbookCore, taskid):
    s = '%d' % taskid
    jobs = pbookCore.getLocalJobList()
    tmp = filter(lambda x: x.jediTaskID==s, jobs)
    if len(tmp) == 1:
        return tmp[0]
    else:
        return None

def findChildJobs(pbookCore, taskid):
    all_jobs = pbookCore.getLocalJobList()
    jobs = []
    for j in all_jobs:
        if j.jediTaskID!='' and int(j.jediTaskID)==taskid:
            jobs.append(j)
    # if len(jobs)>0:
    # In case jobs were resubmitted.
    #     jobs2 = []
    #     for j in jobs:
    #         #print 'Look for children of ', int(j.JobsetID)
    #         v = findChildJobs(pbookCore, int(j.JobsetID))
    #         if len(v)>0: jobs2.extend(v)
    #     # jobs.extend(jobs2)
    #     for j in jobs2:
    #         if j not in jobs:
    #             jobs.append(j)
    return jobs

def updateFromPbook(pbookCore, taskids=[], outDS=''):
    if len(taskids) == 0 and outDS != '':
        all_jobs = pbookCore.getLocalJobList()
        jobs = []
        for j in all_jobs:
            if j.outDS.find(outDS) >= 0:
                taskids.append(int(j.jediTaskID))
        pass
    for tid in taskids:
        log.info('Update from pbook TaskID=%s' % tid)
        jobs = findChildJobs(pbookCore, tid)
        s = 'CHILD_JOBS='
        for j in jobs:
            js_id = int(j.JobsetID)
            keys = j.JobMap.keys()
            keys.sort()
            for jid in keys:
                s += '%d:%d:%d,' % (int(j.jediTaskID), js_id, int(jid))
        print s
    for tid in taskids:
        js = findJobset(pbookCore, tid)
        jsid = js.JobsetID
        for jid, j in js.JobMap.iteritems():
            words = j.jobStatus.split(',')[1:]
            n_defined = words.count('defined') + words.count('activated')
            n_running = words.count('running')
            n_finished = words.count('finished')
            n_failed = words.count('failed')
            n_cancelled = words.count('cancelled')
            st = 'defined:%d,running:%d,finished:%d,failed:%d,cancelled:%d' % \
                 (n_defined, n_running, n_finished, n_failed, n_cancelled)
            print 'JOB_STATUS=taskID:%d,jobsetID:%d,jobID:%d,build:%s,%s' % \
                  (tid, int(jsid), int(jid), j.buildStatus, st)
    pass


#---------------------------------------------------------------------
# Main program
#---------------------------------------------------------------------
def parseOptions():
    op = optparse.OptionParser()

    op.add_option('-f', '--storage-file', dest='storage_file',
                  action='store', default='',
                  help='Storage file for storage (.pickle and later .xml)')

    # control options
    op.add_option('-p', '--file-pattern', dest='file_pattern',
                  action='store', default='',
                  help='Pattern for the filenames in the dataset')

    return op.parse_args()

if __name__ == '__main__':
    options, args = parseOptions()

    if os.path.exists(options.storage_file):
        tm = TaskMgr(filename=options.storage_file)
        tm.load()
    else:
        log.warning('No file found for the task information: ' % \
                    options.storage_file)
        sys.exit(-1)
    pat = options.file_pattern

    dq2i = Dq2Interface()
    for t in tm.tasks:
        v = dq2i.getListOfFilesOnDcache(t, pat, True)
        n = dq2i.numberOfFilesInDataset(t.taskDefinition.outDS+'/', pat)
        nmissing = n - len(v)
        comment = ''
        if nmissing == 0:
            comment = 'All copied'
        else:
            comment = 'Missing %d files' % nmissing
        fname = 'flist_%s.txt' % t.taskDefinition.name
        f = open(fname, 'w')
        f.write('#-------------------------------------------------------\n')
        f.write('# DS: %s\n' % t.taskDefinition.name)
        f.write('# N total=%d, N available=%d (%s)\n' % (n, len(v), comment))
        f.write('#-------------------------------------------------------\n')
        for ds in v:
            f.write('%s\n' % ds)
        f.close()



