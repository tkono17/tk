#!/usr/bin/env python
#-----------------------------------------------------------------------
# Usage: list_sources_under.py <directory_name>
#-----------------------------------------------------------------------
import cmtpack
import os
import sys
import re
import getopt
import datetime

#----------------------------------------------------------------
# Parameters
#-----------
paths = []
ta_value = os.getenv('TestArea')
if ta_value != None:
    paths=ta_value.split(':')
do_archive = False
do_verbose = False
do_list = False
do_subdirs = True
tar_file = ''
#----------------------------------------------------------------


def usage():
    print 'Usage: %s [options]' % sys.argv[0]
    print "Options:"
    print "  -p <paths>   ..... Top directories to scan. Multiple paths should be separated by ':'."
    print "                     (default=$TestArea)"
    print "  -a <filename>..... Name of the archive file."
    print "  -l           ..... Just list the packages to archive without archiving"
    print "  -s [yes|no]  ..... Whether to include the sub-directories of each package"
    print "  -v           ..... Turn on the verbose mode."
    print "  -h           ..... Help."
    print "Examples:"
    print "  %s -a a.tgz -v" % sys.argv[0]

def print_config(paths, do_archive, tar_file, do_list, do_subdirs):
    print 'Top directories to look at: '
    for a in paths:
        print '- ' + a
    yes_no = 'no'
    #
    if do_archive: yes_no = 'yes'
    else: yes_no = 'no'
    print 'Create archive: '+ yes_no
    print 'Archive file: ' + tar_file
    #
    if do_list: yes_no = 'yes'
    else: yes_no = 'no'
    print 'Archive file: ' + yes_no
    #
    if do_subdirs: yes_no = 'yes'
    else: yes_no = 'no'
    print 'List sub-directories of packages: ' + yes_no

def date_string_now():
    now = datetime.datetime.now()
    s = now.strftime("%Y-%m-%d_%H.%M.%S")
    return s

def mk_archive(sources_map, tar_file):
    global do_verbose
    #
    if tar_file=='':
        print 'Warning: no archive file for output specified'
        return -1
    abs_tar_file = os.path.abspath(tar_file)
    tar_opts = "cf"
    if do_verbose: tar_opts += 'v'
    if re.search('\.gz', abs_tar_file) or re.search('\.tgz', abs_tar_file):
        tar_opts += 'z'
    if os.path.exists(abs_tar_file):
        os.rename(abs_tar_file, abs_tar_file+'.bak.'+date_string_now())
    first = True
    curdir = os.getcwd()
    for dir in sources_map.keys():
        os.chdir(dir)
        if first:
            first = False
        else:
            tar_opts.replace('c', 'u')
        command = "tar %s %s" % (tar_opts, abs_tar_file)
        for p in sources_map[dir]:
            command += " " + p
        os.system(command)
    os.chdir(curdir)
    return 0


#----------------------------------------------------------------
# Read options from the command-line arguments
#---------------------------------------------
args = sys.argv[1:]
if len(args)==0:
    usage()
    sys.exit(0)
optval, args = getopt.getopt(args, 'p:a:hvls:')
for opt, val in optval:
    if opt=='-p':
        paths = val.split(':')
    elif opt=='-a':
        do_archive = True
        tar_file = val
    elif opt=='-v':
        do_verbose = True
    elif opt=='-l':
        do_list = True
    elif opt=='-s':
        if val=='yes': do_subdirs = True
        elif val=='no': do_subdirs = False
        else:
            print "Warning: argument to -s options is 'yes' or 'no'. Disable sub-directory listing."
            do_subdirs = False
    elif opt=='-h':
        usage()
        sys.exit(0)
#----------------------------------------------------------------

if len(args)>0:
    print 'Unrecognized arguments : ', args
    sys.exit(0)

if do_verbose:
    print_config(paths, do_archive, tar_file, do_list, do_subdirs)

curdir = os.getcwd()
list_of_sources = {}
for topdir in paths:
    os.chdir(topdir)
    for pack in cmtpack.all_packages_under('.'):
        for s in cmtpack.package_sources(pack.mAbsPath):
            path = os.path.join(pack.mAbsPath, s)
            path = path.replace(topdir+os.sep, '')
            if topdir not in list_of_sources.keys():
                list_of_sources[topdir] = []
            list_of_sources[topdir].append(path)
os.chdir(curdir)

if do_archive:
    status = mk_archive(list_of_sources, tar_file)
    if status != 0:
        for dir in list_of_sources.keys():
            for p in list_of_sources[dir]:
                print os.path.join(dir, p)
elif do_list:
    re_cmt_at_end = re.compile('/cmt$')
    for dir in list_of_sources.keys():
        for p in list_of_sources[dir]:
            pp = p
            is_package = False
            if do_subdirs:
                is_package = True
            else:
                if re_cmt_at_end.search(pp):
                    is_package = True
                    pp = re_cmt_at_end.sub('', pp)
            if not is_package: continue
            print os.path.join(dir, pp)

