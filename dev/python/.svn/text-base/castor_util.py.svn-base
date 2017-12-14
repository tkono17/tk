#!/usr/bin/env python

import os
import sys
import re
import datetime
import getopt

monthname_to_number = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
    }

class CastorInfo:
    def __init__(self):
        self.mode='----------'
        self.second = ''
        self.user = ''
        self.group = ''
        self.size = 0
        self.modified_time = datetime.datetime.now()
        self.name = ''
        self.subs = []
        self.isDir = False
        
    def __init__(self, rfdir_line):
        words = rfdir_line.split()
        if len(words) >= 9:
            self.mode=words[0]
            self.second = words[1]
            self.user = words[2]
            self.group = words[3]
            self.size = int(words[4])
            now = datetime.datetime.now()
            year, month, day, hour, minute = \
                  now.year, now.month, now.day, now.hour, now.minute
            self.modified_time = datetime.datetime(year, month, day, 
                                                   hour, minute)
            self.name = words[-1]
        else:
            print 'Cannot understand as output line from rfdir: ', rfdir_line
            self.mode='----------'
            self.second = ''
            self.user = ''
            self.group = ''
            self.size = 0
            self.modified_time = ''
            self.name = ''
        self.subs = []
        if words[0][0]=='d': self.isDir = True
        else: self.isDir = False
        
    def addEntry(self, x):
        self.subs.append(x)
    def getEntries(self):
        return len(self.subs)

## def exists_castor_dir(path):
##     re_no_file = re.compile('No such file or directory')
##     re_path = re.compile(path)
##     #
##     path_exists = False
##     path_isdir = False
##     command = "rfdir %s 2>&1" % (path)
##     f = os.popen(command, 'r')
##     for line in f.readlines():
##         if re_no_file.search(line):
##             continue
##         elif re_path.search(line):
##             path_exists = True
##             break
##     f.close()
##     if path_exists:
##         one_dir_up = os.path.dirname(path)

def castor_listdir(dirname):
    dirname.rstrip('/')
    re_no_file = re.compile('No such file or directory')
    re_path = re.compile(dirname)
    # Input : [1] CASTOR directory
    #         [2] Listing of CASTOR for the directory specified in [1]
    # Ouptut: Size of the file
    castor_info = None
    castor_listing = []
    path_exists = True
    this_is_a_file = False
    command = "rfdir %s 2>&1" % (dirname)
    f = os.popen(command, 'r')
    for line in f.readlines():
        line = line[:-1]
        if re_no_file.search(line):
            path_exists = False
            continue
        elif re_path.search(line):
            this_is_a_file = True
            castor_listing.append(CastorInfo(line))
        else:
            castor_listing.append(CastorInfo(line))
    f.close()
    # print 'len = ', len(castor_listing)
    if path_exists:
        if this_is_a_file:
            return castor_listing[0]
        else:
            base_name = os.path.basename(dirname)
            one_up = os.path.dirname(dirname)
            one_up_name = os.path.basename(one_up)
            command = "rfdir %s 2>&1" % (one_up)
            f = os.popen(command, 'r')
            for line in f.readlines():
                line = line[:-1]
                if re_no_file.search(line)==None:
                    castor_info = CastorInfo(line)
                    if castor_info.name == base_name:
                        castor_info.name = dirname
                        castor_info.subs = castor_listing
                        break
            f.close()
    return castor_info

def castor_size():
    # Input : Directory listing of CASTOR file or directory.
    # Ouptut: Size of the file
    print 'hi'

def castor_exists(path):
    print 'hi'
    
def castor_isdir(path):
    ci = castor_listdir(path)
    if ci!=None and ci.isDir: return True
    else: return False

def usage():
    print 'Usage: [options] <castor_path>'
    
if __name__ == '__main__':
    optval, args = getopt.getopt(sys.argv[1:], 'ls')
    print optval
    if len(args) == 1:
        castor_path = args[0]
        castor_entry = castor_listdir(castor_path)
        if castor_entry==None:
            print 'Path does not exist: ',castor_path
        else:
            print 'path type (isdir): ', castor_entry.isDir
            for a in castor_entry.subs:
                print "%s, size=%d" % (a.name, a.size)
    else:
        usage()
        
