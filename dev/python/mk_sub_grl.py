#!/usr/bin/env python2.7
#--------------------------------------------------------------------
# Make sub GRL for the given run range [begin, end]
#--------------------------------------------------------------------

import os, sys
import re
import xml.etree.ElementTree as ET
import optparse

def parse_options():
    op = optparse.OptionParser()
    op.add_option('-i', '--input-grl', type='string',
                  dest='input', action='store', default='', 
                  help='Input GRL XML file')
    op.add_option('-o', '--output-grl', type='string',
                  dest='output', action='store', default='', 
                  help='Output GRL XML file')
    op.add_option('--run-begin', type='int', dest='run_begin', action='store',
                  default='-1', 
                  help='The first run number')
    op.add_option('--run-end', type='int',dest='run_end', action='store',
                  default='-1', 
                  help='The last run number')

    return op.parse_args()

def validate_options(opts):
    status = True
    if opts.input == '':
        print 'No input GRL is given : "%s"' % opts.input
        status = False
    if opts.output == '':
        print 'No output GRL is given : "%s"' % opts.output
        status = False
    if opts.run_begin <= 0:
        print 'The first run number is invalid : %d' % opts.run_begin
        status = False
    if opts.run_end <= 0:
        print 'The last run number is invalid : %d' % opts.run_end
        status = False
    if opts.run_end < opts.run_begin:
        print 'The last run number is smaller than the first one'
        status = False
    return status

if __name__ == '__main__':
    opts, args = parse_options()
    if not validate_options(opts):
        sys.exit(-1)

    tree = ET.parse(opts.input)
    root = tree.getroot()
    r2 = root.find('NamedLumiRange')
    if r2 is not None:
        ranges = r2.findall('LumiBlockCollection')
        for r in ranges:
            run = r.find('Run')
            if run is None:
                print 'Cannot find the Run tag in LumiBlockCollection'
                continue
            run_number = int(run.text)
            if run_number >= opts.run_begin and run_number <= opts.run_end:
                #print 'run in range %d' % run_number
                pass
            else:
                r2.remove(r)
    fout = opts.output
    fout2 = '%s.tmp' % fout
    tree.write(fout2)
    # due to stupid feature of GoodRunsList parser
    f2 = open(fout2, 'r')
    f = open(fout, 'w')
    re0 = re.compile('<LBRange End="(\d+)" Start="(\d+)"')
    for line in f2.readlines():
        if len(line)>0 and line[-1]==os.linesep: line = line[:-1]
        mg = re0.search(line)
        if mg:
            start = int(mg.group(2))
            end = int(mg.group(1))
            #print 'start=%d end=%d' % (start, end)
            f.write('<LBRange   Start="%d" End="%d"/>\n' % (start, end) )
        else:
            f.write('%s\n' % line)
        pass
    f2.close()
    f.close()
    os.system('rm %s' % fout2)

    
