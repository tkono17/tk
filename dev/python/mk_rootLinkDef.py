#!/usr/bin/env python
import sys, os
import re

class_name = ''
name_space = ''
over_write = 0

def usage():
    print """
Usage: sys.argv[0] ClassName [options]
Options: -f: force to overwrite the output file.
         --ns=: set namespace if any. (Currently only supports namespace
                with only 1 depth, e.g. myns::
Example: mk_rootLinkDef.py MyClass [-f -ns=myns]
    """
    
if len(sys.argv)<2:
    usage()
    sys.exit(0)

def get_option(arg):
    global name_space
    global over_write
    if re.match('--ns=',tmp)!=None:
        name_space = tmp[5:]
    elif tmp=='-f':
        over_write = 1

class_name = sys.argv[1]
if len(sys.argv)>2:
    for i in range(2,len(sys.argv)):
        tmp = sys.argv[i]
        get_option(tmp)

print 'name_space = '+name_space
print 'overwrite = ',over_write

file_name = class_name+'LinkDef.hxx'

if os.path.exists(file_name):
    if over_write!=0: os.remove(file_name)
    else:
        print 'File '+file_name+ ' exists'
        sys.exit(0)

# Create the <ClassName>LinkDef.hxx file and write to it.
file = open(file_name, 'w')
if len(name_space)>0:
    file.write('#ifndef __'+name_space+'_'+class_name+'LinkDef_hxx__\n')
    file.write('#define __'+name_space+'_'+class_name+'LinkDef_hxx__\n')
else:
    file.write('#ifndef __'+class_name+'LinkDef_hxx__\n')
    file.write('#define __'+class_name+'LinkDef_hxx__\n')    
file.write('/*\n')
file.write('  '+class_name+'LinkDef.hxx\n')
file.write('*/\n')
file.write('\n')
file.write('#ifdef __CINT__\n')
file.write('#pragma link off all globals;\n')
file.write('#pragma link off all functions;\n')
file.write('#pragma link off all classes;\n')
if len(name_space)>0:
    file.write('#pragma link C++ namespace '+name_space+';\n')
    file.write('#pragma link C++ class '+name_space+'::'+class_name+'+;\n')
else:
    file.write('#pragma link C++ class '+class_name+'+;\n')
file.write('#endif // __CINT__\n')
file.write('\n')
file.write('#endif\n')
file.close()
