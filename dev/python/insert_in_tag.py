#!/usr/bin/env python
#----------------------------------------------------------------------

import os, sys
import re
import getopt

#----------------------------------------------------------------------
# Parameters
TAG_PREFIX='^#TAG'
jo_file_base=''
jo_file_new=''
hook_file=''
do_dump=False
verbose = False

# Secondary parameters
jo_hooks = {}

#----------------------------------------------------------------------
# Functions
def usage():
    print 'Usage: %s [Options] <base> <out> <hook_file>' % (sys.argv[0])
    print """--------
Inserts lines specified in the <hook_file> between <key>_begin and <key>_end
after the line which looks like "<tag>-<key>" in the original <base> file.
--------
Options: -t <tag> ... Tag prefix in the original file [^#TAG]
         -v       ... Verbose
"""

def dump_hooks(hooks):
    for key in hooks.keys():
        print '***** %s' % key
        for line in hooks[key]:
            print '     %s' % line
        print '**********'

#----------------------------------------------------------------------
# Read arguments
opts, args = getopt.getopt(sys.argv[1:], 't:v', ['--tag', '--verbose'])
for opt, value in opts:
    if opt in ['-t', '--tag']:
        TAG_PREFIX = value
    elif opt in ['-v', '--verbose']:
        verbose = True
        
if len(args)!=3:
    usage()
    sys.exit(1)
jo_file_base = args[0]
jo_file_new = args[1]
hook_file= args[2]

#print jo_file_base, jo_file_new, hook_file
#----------------------------------------------------------------------
# Main
# re_hook = re.compile('^(\w+)\s*=\s*([\w\[\]\'\"\s\.,]+)')
re_hook_begin = re.compile('([\w_-]+)_begin')
re_hook_end = re.compile('([\w_-]+)_end')
re_jo_hook = re.compile('%s-([\w_-]+)' % TAG_PREFIX)

f_hook = open(hook_file, 'r')
is_reading_hook=False
for line in f_hook.readlines():
    if len(line)>0: line = line[:-1]
    if not is_reading_hook:
        mg = re_hook_begin.match(line)
        if mg:
            key = mg.group(1)
            is_reading_hook = True
            if key in jo_hooks.keys():
                print "Replacing HOOK for TAG '%s'" % key
                jo_hooks[key] = []
            else:
                jo_hooks[key] = []
    else:
        mg = re_hook_end.match(line)
        if mg:
            is_reading_hook = False
        else:
            jo_hooks[key].append(line)
f_hook.close()

if do_dump or verbose: dump_hooks(jo_hooks)

f_jo_base = open(jo_file_base, 'r')
f_jo_new = open(jo_file_new, 'w')
for line in f_jo_base.readlines():
    mg = re_jo_hook.match(line)
    doit=False
    if mg:
        key = mg.group(1)
        if key in jo_hooks.keys():
            doit = True
        else:
            print "TAG '%s' found in base file but not specified in HOOK" % key
    f_jo_new.write(line)
    if doit:
        for ll in jo_hooks[key]:
            f_jo_new.write('%s\n' % (ll))
f_jo_base.close()
f_jo_new.close()
