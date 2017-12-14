#!/usr/bin/python2.2
#--------------------------------------------------------------------------
# Python module zjm
#---------------------
# Zeus Job Manager module
#--------------------------------------------------------------------------
import os
import sys
import string
import time
import re
import zjm_config

## job_dir = zjm_config.job_dir
## dir_oubbox  = job_dir + '/Outbox'
## dir_sentbox = job_dir + '/Sentbox'
## dir_inbox   = job_dir + '/Inbox'
## dir_log     = job_dir + '/Log'

def outbox():
    return zjm_config.job_dir + '/Outbox'
def sentbox():
    return zjm_config.job_dir + '/Sentbox'
def inbox():
    return zjm_config.job_dir + '/Inbox'
def log():
    return zjm_config.job_dir + '/Log'

#--------------------------------------------------------------------------
# job sub/get/purge commands which should be used with the '.jobinfo' file
# as the input.
#--------------------------------------------------------------------------
def do_jobsub(filename, test=0):
    job_info = JobInfo()
    job_info.readFile(filename)
    dir_sav = os.getcwd()
    os.chdir(job_info.workDir())
    jobsub(job_info.script(), job_info.queue(), 
           job_info.inputFiles(), job_info.jobName(), 
           job_info.hostName(), test)
    job_info.values['job_id'] = get_jobsubid('jobsub.out')
    os.chdir(dir_sav)
    if job_info.values['job_id']<0:
        return
    append_jobsub_out(filename, job_info.jobID())
    filename_new = "../Sentbox/%s" % filename
    os.rename(filename, filename_new)
    
def do_jobget(filename, test=0):
    job_info = JobInfo()
    job_info.readFile(filename)
    dir_sav = os.getcwd()
    os.chdir(job_info.workDir())
    jobget(job_info.jobID(), job_info.outputFiles(), test)
#    get_jobget_status('jobget.out')
    os.chdir(dir_sav)
    append_jobget_out(filename, job_info.jobID())
    filename_new = "../Inbox/%s" % filename
    os.rename(filename, filename_new)
    
def do_jobpurge(filename, test=0):
    job_info = JobInfo()
    job_info.readFile(filename)
    dir_sav = os.getcwd()
    os.chdir(job_info.workDir())
    jobpurge(job_info.jobgetID(), test)
    os.chdir(dir_sav)
    append_jobsub_out(filename, job_info.jobgetID())

#--------------------------------------------------------------------------
# Internal data structure used to store information in the '.jobinfo' file.
#--------------------------------------------------------------------------
class JobInfo:
    def __init__(self):
        self.values = {}
        self.keywords =(
            'script',
            'queue',
            'control_cards', 'shared_library',
            'input_file', 'input_files', 
            'output_file', 'output_files', 
            'jobname',
            'hostname',
            'job_id', 'jobget_id', 
            'jobsub_date', 'jobget_date', 'jobpurge_date',
            'work_dir'
            )
        for a in self.keywords:
            self.values[a] = ''
        self.values['script'] = 'eaze_run.sh'
        self.values['queue'] = 'M'
        self.values['input_file'] = ''
        self.values['output_file'] = ''
        self.values['input_files'] = []
        self.values['output_files'] = []
        self.values['jobname'] = 'eaze_example'
        self.values['hostname'] = 'zenithsub'
        self.values['job_id'] = 0
        self.values['jobget_id'] = 0
        self.values['jobsub_date'] = ''
        self.values['jobget_date'] = ''
        self.values['jobpurge_date'] = ''
        self.values['work_dir'] = '.'

    def script(self):
        return self.values['script']
    def queue(self):
        return self.values['queue']
    def inputFiles(self):
        return self.values['input_files']
    def outputFiles(self):
        return self.values['output_files']
    def jobName(self):
        return self.values['jobname']
    def hostName(self):
        return self.values['hostname']
    def jobID(self):
        return self.values['job_id']
    def jobgetID(self):
        return self.values['jobget_id']
    def jobsubDate(self):
        return self.values['jobsub_date']
    def jobgetDate(self):
        return self.values['jobget_date']
    def jobpurgeDate(self):
        return self.values['jobpurge_date']
    def controlCards(self):
        return self.values['control_cards']
    def workDir(self):
        return self.values['work_dir']

    def readFile(self, filename):
        myfile = open(filename, 'r')
        for a in myfile.readlines():
            if len(a)==0 or a[0]=='#': continue
            kv = a[:-1].split()
            if len(kv) >= 2:
                key = kv[0]
                value = kv[1]
            elif len(kv) > 2:
                key = kv[0]
                values = kv[1:]
            else:
                continue
#            print 'key = ', key, ', value = ', value
            if key in self.keywords:
                if key=='input_file' or key=='control_cards' \
                       or key=='shared_library':
                    self.values['input_files'].append(value)
                    if key=='control_cards': self.values[key] = value
                elif key == 'input_files':
                    self.values['input_files'].extend(values)
                elif key == 'output_file':
                    self.values['output_files'].append(value)
                elif key == 'output_files':
                    self.values['output_files'].extend(values)
                else:
                    self.values[key] = value
        myfile.close()
        if self.values['job_id']!='' and self.values['job_id']!=0:
            self.values['job_id'] = int(self.values['job_id'])
        if self.values['jobget_id']!='' and self.values['jobget_id']!=0:
            self.values['jobget_id'] = int(self.values['jobget_id'])
    def dump(self):
        for a in self.keywords:
            if a=='input_file' or a=='output_file': continue
            print a, ' = ', self.values[a]
    
def jobsub(script, queue, input_files, jobname='', 
           hostname='zenithsub', test=1):
    if script == '': return ''
    line = 'jobsub'
    if queue != '': line = "%s -q %s" % (line, queue)
    if hostname != '' : line = "%s -h %s" % (line, hostname)
    if jobname != '' : line = "%s -j %s" % (line, jobname)
    if script !='': line = "%s %s" % (line, script)
    if len(input_files) > 0: line = "%s -f " % line
    for a in input_files:
        line = "%s %s" % (line, a)
    line = "%s > jobsub.out" % line
    if test != 0:
        print '\nI will submit the job with the following command => \n'
        print '\'' + line + '\''
        print ''
    else:
        os.system(line)
    return line

def jobget(jobid, output_files, test=1):
    line = "jobget %d" % jobid
    if len(output_files) > 0: line = "%s -f " % line
    for a in output_files:
        line = "%s %s" % (line, a)
    line = "%s > jobget.out" % line
    if test != 0:
        print '\nI will get the job with the following command => \n'
        print '\'' + line + '\''
        print ''
    else:
        os.system(line)
    return
    
def jobpurge(jobid, test):
    line = "jobpurge %d" % (jobid)
    line = "%s > jobpurge.out" % line
    if test != 0:
        print '\nI will purge the job with the following command => \n'
        print '\'' + line + '\''
        print ''
    else:
        os.system(line)
    return


def get_jobsubid(filename):
    fp = open(filename, 'r')
    lines = fp.readlines()
    fp.close()
    if len(lines) != 1: return -1
    a = lines[0].split()
    return int(a[1])

def get_jobget_status(filename):
    ok = 0
    fp = open(filename, 'r')
    re_success = re.compile('Successfully run')
    for a in fp.readlines():
        if re_success.search(a):
            ok = 1
            break
    fp.close()
    return ok

def append_jobsub_out(filename, jobid):
    t = time.localtime()
    line = time.strftime("%a %b %d %H:%M:%S %Z %Y", t)
    line = "# %s\n" % line
    fp = open(filename, 'a')
    fp.write('\n')
    fp.write('#---------------------------------------------------\n')
    fp.write('# jobsub done on\n')
    fp.write(line)
    fp.write('#---------------------------------------------------\n')
    line = "job_id     %d\n" % jobid
    fp.write(line)
    fp.write('#---------------------------------------------------\n')
    fp.close()

def append_jobget_out(filename, jobid):
    t = time.localtime()
    line = time.strftime("%a %b %d %H:%M:%S %Z %Y", t)
    line = "# %s\n" % line
    fp = open(filename, 'a')
    fp.write('\n')
    fp.write('#---------------------------------------------------\n')
    fp.write('# jobget done on\n')
    fp.write(line)
    fp.write('#---------------------------------------------------\n')
    line = "jobget_id     %d\n" % jobid
    fp.write(line)
    fp.write('#---------------------------------------------------\n')
    fp.close()

def find_jobinfo():
    fs = os.listdir('.')
    re_jobinfo = re.compile('\.jobinfo')
    for a in fs:
        if re_jobinfo.search(a):
            return a
    return ''

def mk_dir_cards(file_jobinfo):
    subdirs = mk_dirs()
    sav_dir = os.getcwd()
    bname_jobinfo = os.path.basename(file_jobinfo)
    bname_jobinfo.replace(r'.jobinfo', '')
    for a in subdirs:
        l = "cp %s %s/%s_%s.jobinfo" % (file_jobinfo, a, bname_jobinfo, a)
        print l
        os.system(l)
        os.chdir(a)
        l = "%s_%s.jobinfo" % (bname_jobinfo, a)
        update_jobinfo(l)
        os.chdir(sav_dir)

def mk_dirs():
    # Search for the current directory (where the script was executed)
    # and find the fragment of control.cards (which contains input files
    # for one job), with the name 'control.cards.[suffix]'. From these control
    # cards, create subdirectory, '[suffix]' and move the control
    # cards to that subdirectory. End.
    dir_listing = os.listdir('.')
    sav_dir = os.getcwd()
    files = []
    subdirs = []
    re_cards = re.compile('^control\.cards\..')
    re_bak = re.compile('~$')
    for a in dir_listing:
        if os.path.isfile(a) and re_cards.search(a) and not re_bak.search(a):
            files.append(a)
    for a in files:
        suffix = a.replace(r'control.cards.', '')
        subdirs.append(suffix)
        new_name = "%s/%s" % (suffix, a)
        if not os.path.exists(suffix):
            os.mkdir(suffix)
        elif not os.path.isdir(suffix):
            print suffix, 'is not a directory, remove it and mkdir'
            os.remove(suffix)
            os.mkdir(suffix)
        os.rename(a, new_name)
        os.chdir(suffix)
        os.chdir(sav_dir)
    return subdirs

def update_jobinfo(file_jobinfo):
    # Given the '.jobinfo' file, update parameters 'work_dir',
    # 'control_cards' to proper values.
    tmp_f_name = 'tmp_jobinfo__'
    job_file = open(file_jobinfo, 'r')
    out_file = open(tmp_f_name, 'w')
    control_cards_ok = 0
    work_dir_ok = 0
    control_cards_line = "control_cards     %s/control.cards\n" % os.getcwd()
    work_dir_line = "work_dir          %s\n" % os.getcwd()
    for line in job_file.readlines():
        if len(line)<1 or line[0]=='#':
            out_file.write(line)
            continue
        line = line[:-1]
        words = line.split()
        if len(words)<2:
            a = "%s\n" % line
        elif words[0] == 'control_cards':
            a = control_cards_line
            control_cards_ok = 1
        elif words[0] == 'work_dir':
            a = work_dir_line
            work_dir_ok = 1
        else:
            a = "%s\n" % line
        out_file.write(a)
    if control_cards_ok==0 or work_dir_ok==0:
        out_file.write("\n")
        out_file.write("#------------------------------------------------\n")
        out_file.write("# Following lines generated by update_jobinfo()\n")
        out_file.write("#------------------------------------------------\n")
        if control_cards_ok == 0:
            out_file.write(control_cards_line)
        if work_dir_ok == 0:
            out_file.write(work_dir_line)
        out_file.write("#------------------------------------------------\n")
    job_file.close()
    out_file.close()
    # Rename file etc.
    sav_name = file_jobinfo + '.sav'
    if os.path.exists(sav_name): os.remove(sav_name)
    os.rename(file_jobinfo, sav_name)
    os.rename(tmp_f_name, file_jobinfo)


#--------------------------------------------------------------------------
# MAIN function
#--------------------------------------------------------------------------
if __name__ == '__main__':
    print 'hi'
#    do_jobsub('test.jobinfo', 1)
#    do_jobget('test.jobinfo', 1)
#    do_jobpurge('test.jobinfo', 1)

