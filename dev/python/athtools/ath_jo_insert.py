#!/usr/bin/env python
#----------------------------------------------------------------------

import os, sys
import re

#----------------------------------------------------------------------
# Parameters
jo_file_base=''
jo_file_new=''
hook_file=''

# Secondary parameters
jo_hooks = {}

#----------------------------------------------------------------------
# Functions
def usage():
    print 'Usage: %s <jo_base> <jo_out> <hook_file>' % (sys.argv[0])
    print '  Inserts lines specified in the <hook_file> between'
    print ' <key>_begin and <key>_end' 
    print ' after the line which looks like "#JO_INSERT-<key>" '
    print ' in the original JO file'

def dump_hooks(hooks):
    for key in hooks.keys():
        print '%s: %s' % (key, hooks[key])

#----------------------------------------------------------------------
# Read arguments

if len(sys.argv)!=4:
    usage()
    sys.exit(0)

if len(sys.argv)>1: jo_file_base = sys.argv[1]
if len(sys.argv)>2: jo_file_new = sys.argv[2]
if len(sys.argv)>3: hook_file = sys.argv[3]
    
#----------------------------------------------------------------------
# Main
# re_hook = re.compile('^(\w+)\s*=\s*([\w\[\]\'\"\s\.,]+)')
re_hook_begin = re.compile('^([\w_-]+)_begin')
re_hook_end = re.compile('^([\w]+)_end')
re_jo_hook = re.compile('^#JO_INSERT-([\w_-]+)')

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
                print "Replacing JO_HOOK '%s'" % key
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

dump_hooks(jo_hooks)

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
            print "JO_HOOK '%s' found in JO but you didn't specify it" % key
    f_jo_new.write(line)
    if doit:
        for ll in jo_hooks[key]:
            f_jo_new.write('%s\n' % (ll))
f_jo_base.close()
f_jo_new.close()
