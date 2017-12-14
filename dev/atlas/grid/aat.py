#!/usr/bin/env python
#-------------------------------------------------------------------
# aat.py: Atlas Athena Tool
#-------------------------------------------------------------------
import os, sys
import re
import tklog

aatlog = 'logs/aat.log'

def parseFile(f    ):
    lines = []
    from_previous=False
    oneline = ''
    for line in f.readlines():
        if len(line)>0: line = line[:-1]
        if from_previous:
            from_previous = False
        else:
            oneline = ''
        #
        isharp = line.find('#')
        if isharp>=0: line = line[:isharp]
        #
        ibslash = line.find('\\')
        if ibslash>=0:
            line = line[:ibslash]
            from_previous = True
        oneline += line
        if not from_previous:
            if len(oneline)>0: lines.append(oneline)
    return lines

class KeyValue:
    def __init__(self, key):
        self.Key = key
        self.Name = ''
    def key(self, key=None):
        if key!=None: self.Key = key
        return self.Key
    def name(self, name=None):
        if name!=None: self.Name = name
        return self.Name
    def isValidName(self, name):
        return (name!=None and name!='')
    def set(self, name):
        self.Name = name
    def __str__(self):
        s = '%-25s: %-25s' % (self.Key, self.Name)
        return s

class KeyArray(KeyValue):
    def __init__(self, key):
        self.Key = key
        self.Values = []
    def key(self, key=None):
        if key!=None: self.Key = key
        return self.Key
    def values(self, values=[]):
        values = values
        return self.Values
    def n(self):
        return len(values)
    def set(self, values):
        self.Values = values
    def __str__(self):
        s = '%-25s:' % self.Key
        for a in self.Values:
            s += ' %-25s' % a
        return s
    
class TemplatedFileValue(KeyValue):
    def __init__(self, key):
        KeyValue.__init__(self, key)
        self.TemplateName = None
        self.HooksName = None
    def template(self, fname=None):
        if fname!=None: self.TemplateName = fname
        return self.TemplateName
    def hooks(self, fname=None):
        if fname!=None: self.HooksName = fname
        return self.HooksName
    def set(self, name, srcs):
        KeyValue.set(self, name)
        if srcs!=None:
            if len(srcs)>0: self.TemplateName = srcs[0]
            if len(srcs)>1: self.HooksName = srcs[1]
    def update(self, tag):
        if self.isValidName(self.Name) and \
           self.isValidName(self.TemplateName) and \
           self.isValidName(self.HooksName):
            command = 'insert_in_tag.py -t "%s" %s %s %s' % \
                      (tag, self.TemplateName, self.Name, self.HooksName)
            tklog.system(command, aatlog)
        else:
            print 'Name: ', self.isValidName(self.Name)
            print 'TemplateName: ', self.isValidName(self.TemplateName)
            print 'HooksName: ', self.isValidName(self.HooksName)
            
    def __str__(self):
        s = KeyValue.__str__(self)
        if self.isValidName(self.TemplateName) or \
               self.isValidName(self.HooksName):
            s += ' <-'
        if self.isValidName(self.TemplateName): s +=' %s' % self.TemplateName
        if self.isValidName(self.HooksName): s +=' %s' % self.HooksName
        return s
    
class JobConf:
    def __init__(self):
        self.KeyValues = {}
        self.KeyArrays = {}
        self.TemplatedFileValues = {}
        self.WorkDir = self.createKeyValue('work_dir')
        self.LxbatchWorkDir = self.createKeyValue('lxbatch_work_dir')
        self.JobType = self.createKeyValue('job_type')
        self.Dataset = self.createKeyValue('dataset')
        self.JobOptions = self.createTemplatedFileValue('jobOptions_file')
        self.JdlFile    = self.createTemplatedFileValue('jdl_file')
        self.Script     = self.createTemplatedFileValue('script_file')
        self.Hooks      = self.createTemplatedFileValue('job_hooks_file')
        self.RunScript  = self.createKeyValue('run_script')
        # LXBATCH
        self.JobInputFiles = self.createKeyArray('job_input_file')
        self.CmtTag = self.createKeyValue('cmttag')
        self.CE = self.createKeyValue('CE')
    def createKeyValue(self, key):
        a = None
        if key in self.KeyValues.keys():
            a = self.KeyValues[key]
        else:
            a = KeyValue(key)
            self.KeyValues[key] = a
        return a
    def createKeyArray(self, key):
        a = None
        if key in self.KeyArrays.keys():
            a = self.KeyArrays[key]
        else:
            a = KeyArray(key)
            self.KeyArrays[key] = a
        return a
    def createTemplatedFileValue(self, key):
        a = None
        if key in self.TemplatedFileValues.keys():
            a = self.TemplatedFileValues[key]
        else:
            a = TemplatedFileValue(key)
            self.TemplatedFileValues[key] = a
        return a
    def read(self, fname):
        re_fft = re.compile('([^=]+)=([^<]+)(?:<-(.+))?')
        f = open(fname, 'r')
        for line in parseFile(f):
            if len(line)>0 and line[-1]=='\n': line = line[:-1]
            if len(line)>0 and line[0]=='#': continue
            line2 = re.sub('\s', '', line)
            # print 'line2=%s' % line2
            mg = re_fft.match(line2)
            if mg==None: continue
            (key, value, srcs) = mg.groups()
            if srcs:
                srcs = srcs.split(',')
            # print '%-20s: "%s" is made of %s' % (key, value, srcs)
            if key in self.KeyValues.keys():
                self.KeyValues[key].set(value)
            elif key in self.KeyArrays.keys():
                self.KeyArrays[key].set(value.split(','))
            elif key in self.TemplatedFileValues.keys():
                self.TemplatedFileValues[key].set(value, srcs)
        f.close()
    def printIt(self):
        for a in self.KeyValues.values():
            print a
        for a in self.KeyArrays.values():
            print a
        for a in self.TemplatedFileValues.values():
            print a

if __name__ == '__main__':
    jc = JobConf()
    jc.read('jobconf.txt')
    
