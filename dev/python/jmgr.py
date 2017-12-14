#!/usr/bin/env python
#----------------------------------------------------------
# jmgr.py
# Job manager in a local PC cluster (pcatlasXXX)
#----------------------------------------------------------

import os
import re

jobpool_waiting = '/space/tkohno/work/jobpool/waiting'
jobpool_running = '/space/tkohno/work/jobpool/running'
jobpool_done = '/space/tkohno/work/jobpool/done'
jobpool_failed = '/space/tkohno/work/jobpool/failed'

working_dir_default = '/space/tkohno/work/jobpool/run'

class JobInfo:
    def __init__(self):
        self._job_name = ''
        self._setup_script = ''
        self._executable = ''
        self._working_dir = working_dir_default
        self._output_files = []
        pass
    def readFromFile(self, fname):
        print 'fname: ', fname
        if os.path.exists(fname):
            print 'hi'
            self._job_name = os.path.basename(fname)
            f = open(fname, 'r')
            re_kv = re.compile('([^\s]+)\s*:\s*([^\s]+)')
            for line in f.readlines():
                if len(line)>0: line = line[:-1]
                mg = re_kv.search(line)
                if mg:
                    (key, value) = mg.groups()
                    if key == 'setup_script' and value!='':
                        self._setup_script = value
                    if key == 'executable':
                        self._executable = value
                    if key == 'working_dir' and value!='':
                        self._working_dir = value
                    if key == 'output_files':
                        self._output_files = value.split(',')
        pass
    def job_name(self):
        return self._job_name
    def executable(self):
        return self._executable
    def setup_script(self):
        return self._setup_script
    def working_dir(self):
        return self._working_dir
    def output_files(self):
        return self._output_files
    def printIt(self):
        print 'job_name    : %s' % self._job_name
        print 'working_dir : %s' % self._working_dir
        print 'setup_script: %s' % self._setup_script
        print 'executable  : %s' % self._executable
        print 'output_files: %s' % str(self._output_files)
        
    
def check_requests():
    print 'checking new job requests in %s' % jobpool_waiting
    files = os.listdir(jobpool_waiting)
    print 'new requests: ', files
    curdir = os.getcwd()
    os.chdir(jobpool_waiting)
    for f in files:
        if not (f.startswith('.') or f.endswith('~')):
            print 'Reading %s' % f
            ji = JobInfo()
            ji.readFromFile(f)
            ji.printIt()
            name = ji.job_name()
            if ji.job_name() != '':
                run_job(ji)
                os.rename('%s/%s' % (jobpool_waiting, name), 
                          '%s/%s' % (jobpool_running, name))
    os.chdir(curdir)
    pass

def check_status():
    print 'checking status of jobs in %s' % jobpool_running
    files = os.listdir(jobpool_running)
    print 'list of jobs: ', files
    curdir = os.getcwd()
    os.chdir(jobpool_running)
    for f in files:
        if not (f.startswith('.') or f.endswith('~')) and f.endswith('.txt'):
            print 'checking file', f
            ji = JobInfo()
            ji.readFromFile(f)
            name = ji.job_name()
            ji.printIt()
            if os.path.isdir(ji.working_dir()):
                if os.path.exists('%s/success' % ji.working_dir()):
                    os.rename('%s/%s' % (jobpool_running, name), 
                              '%s/%s' % (jobpool_done, name))
                elif os.path.exists('%s/failed' % ji.working_dir()):
                    os.rename('%s/%s' % (jobpool_running, name), 
                              '%s/%s' % (jobpool_failed, name))
            else:
                print 'Cannot find job in %s' % ji.working_dir()
    os.chdir(curdir)
    pass
    
def run_job(jobinfo):
    print 'Run job: ', jobinfo.job_name()
    if not os.path.isdir(jobinfo.working_dir()):
        os.mkdir(jobinfo.working_dir())
    curdir = os.getcwd()
    os.chdir(jobinfo.working_dir())
    #
    f = open('run_script.sh', 'w')
    f.write('#!/usr/bin/env zsh\n\n')
    if jobinfo.setup_script()!='':
        if os.path.exists(jobinfo.setup_script()):
            f.write(jobinfo.setup_script() + '\n')
        else:
            log.warning('Setup script does not exist: %s' % \
                        jobinfo.setup_script())
    if jobinfo.executable()!='':
        if os.path.exists(jobinfo.executable()):
            f.write(jobinfo.executable() + '\n')
        else:
            log.warning('Executable does not exist: %s' % jobinfo.executable())
    f.write
    f.write('\n')
    f.write('if [[ $? == 0 ]]; then\n')
    f.write('    echo "Job finished successfully"\n')
    f.write('    touch success\n')
    f.write('else\n')
    f.write('    echo "Job failed"\n')
    f.write('    touch failed\n')
    f.write('fi\n')
    f.close()
    os.system('chmod +x run_script.sh')
    os.system('./run_script.sh >& job.out')
    os.chdir(curdir)
    pass

def update_status():
    pass

def list_status():
    def dir_summary(dname, title):
        files = filter(lambda x: x.endswith('.txt'), os.listdir(dname))
        print '%-10s: %4d jobs' % (title, len(files))
    dir_summary(jobpool_waiting, 'Waiting')
    dir_summary(jobpool_running, 'Running')
    dir_summary(jobpool_done, 'Done')
    dir_summary(jobpool_failed, 'Failed')
    pass


if __name__ == '__main__':
    list_status()
    #Bcheck_status()
    #check_requests()
    
