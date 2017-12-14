#!/usr/bin/env python
#--------------------------------------------------------------
# Find out datasets given a good run list
#--------------------------------------------------------------

import os, sys
import re
import xml.dom.minidom
import commands
import getopt

grl_fname='MyLBCollection.xml'
output_fname='grl_ds.py'
fname_text='grl.txt'

ptag='data09_900GeV'
stream='physics_MinBias'
type='.ESD'

output_dir='.'
job_name='GridJob'
job_version='v1'
do_dump=False
exclude_tags = []
reco_tags = []

def usage():
    print 'Usage: %s' % sys.argv[0]
    print """------
Options:
-f, --file <file> ............ Input Good run list file (xml)
-d, --dump <file> ............ Dump to text file
-o, --output <output_file> ... Output file name
-p, --ptag <ptag> ............ Project tag (needed to select dataset from run)
-s, --stream <stream> ........ Stream (needed to select dataset from run)
-t, --dataset_type <type> .... Dataset type (regex, .AOD, .ESD, etc.)
-j, --job_name <name> ........ Job name (used to set the output DS name)
-v, --job_version <version> .. Job version, e.g. v1, v2, ...
    --reco-tags <reco_tag> .... Preferred list of reco tags (comma-separated list)
-x, --exclude_tags <reco_tag>. Exclude datasets with reco tag <> (, sep. list)
-h, --help ................... Help
"""

def dumpGRL(et_root, fname):
    lbcs = et_root.findall('NamedLumiRange/LumiBlockCollection')
    fout = open(fname, 'w')
    for lbc in lbcs:
        runs = lbc.findall('Run')
        lbs = lbc.findall('LBRange')
        if not (len(runs) == 1 and len(lbs) >= 1): continue
        run = int(runs[0].text)
        fout.write('# Run %08d\n' % run)
        for lb in lbs:
            LBstart = int(lb.get('Start'))
            LBend = int(lb.get('End'))
            fout.write('%8d %8d %8d\n' % (run, LBstart, LBend))
    fout.close()

def shToPy(sh_file, py_file):
    pass
def pyToSh(sh_file, py_file):
    pass

optval, args = getopt.getopt(sys.argv[1:],
                             'd:f:o:p:s:t:j:v:x:h',
                             ['dump',
                              'file', 'output_file', 
                              'ptag=', 'stream=', 'dataset_type=',
                              'job_name', 'job_version=',
                              'exclude_tags=',
                              'reco-tags=',
                              'help'])

for a in optval:
    opt = a[0]
    val = a[1]
    # print 'checking opt=%s, val=%s' % (opt, val)
    if opt in ('-f', '--file'):
        grl_fname=val
    elif opt in ('-o', '--output_file'):
        output_fname=val
    elif opt in ('-p', '--ptag'):
        ptag=val
    elif opt in ('-d', '--dump'):
        do_dump=True
        fname_text=val
    elif opt in ('-s', '--stream'):
        stream=val
    elif opt in ('-t', '--dataset_type'):
        type=val
    elif opt in ('-j', '--job_name'):
        job_name=val
    elif opt in ('-v', '--job_version'):
        job_version=val
    elif opt in ('-x', '--exclude_tags'):
        exclude_tags=val.split(',')
    elif opt in ('--reco-tags'):
        reco_tags = val.split(',')
    elif opt in ('-h', '--help'):
        usage()
        sys.exit(0)

runs=[]
run_to_ds={}
run_to_allds={}

if not os.path.exists(grl_fname):
    print 'Warning: GoodRunList file %s does not exist' % grl_fname
    sys.exit(-1)
    
if do_dump:
    import xml.etree.cElementTree as ET
    e = ET.parse(grl_fname)
    dumpGRL(e.getroot(), fname_text)
    sys.exit(0)

print 'Reading GRL XML file : %s' % grl_fname
doc = xml.dom.minidom.parse(grl_fname)
run_nodes = doc.getElementsByTagName('Run')
for n in run_nodes:
    if len(n.childNodes) == 1:
        runs.append(int(n.childNodes[0].data))
runs.sort()

for run in runs:
    print 'Find datasets for run (ptag=%s, stream=%s, run=%08d, type=%s)' % \
          (ptag, stream, run, type)
    ds_pattern = '%s.%08d.%s.*%s*' % (ptag, run, stream, type)
    # print 'ds pattern = ', ds_pattern
    command = 'dq2-ls %s |sort -r' % ds_pattern
    # print 'Checking with %s' % command
    output = commands.getoutput(command)
    # print output
    output = output.split(os.linesep)
    if len(output) > 0:
        run_to_allds[run] = output
        run_to_ds[run] = []
        for o in output:
            if o.find('_tid') == -1:
                run_to_ds[run].append(o)
    else:
        print 'No dataset found for "%s", dq2-ls output=%s' % \
              (ds_pattern, output)

fout = open(output_fname, 'w')

#fout.write('typeset -A datasets\n')
#fout.write('datasets=(\n')
fout.write('datasets = {\n')
for r in runs:
    if r in run_to_ds.keys():
        ds_all = run_to_ds[r]
        print ds_all
        #fout.write('    run%08d\n' % r)
        fout.write("    'run%08d' : \n" % r)
        iselected = -1
        comment_out = '# '
        ibest = -1
        for i, x in enumerate(ds_all):
            if ibest >= 0: break
            for tag in reco_tags:
                if x.find(tag) >= 0:
                    ibest = i
                    break
        for i, x in enumerate(ds_all):
            to_be_excluded = False
            for tmp in exclude_tags:
                if x.find(tmp) >= 0:
                    to_be_excluded = True
                    break
            if ibest >= 0:
                if i == ibest:
                    iselected = i
                    comment_out = ''
                else:
                    comment_out = '# '
            else:
                if iselected >= 0 or to_be_excluded:
                    comment_out = '# '
                else:
                    comment_out = ''
                    iselected = i
            fout.write("    %s'%s', \n" % (comment_out, x))
            pass
        if iselected < 0:
            fout.write('    ""\n')
        fout.write('\n')
fout.write('    }\n\n')
#fout.write('keys=(`echo ${(k)datasets} | sed "s/ /\\n/g"| sort`)\n')
for r in runs:
    if r not in run_to_ds.keys():
        print '# No dataset for run %08d'


