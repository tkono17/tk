#!/usr/bin/env python

import os, sys
import re

def usage():
    print "Usage: %s <eventlist.txt>"
    print """------
  Reads the event list file and writes out entries separately in
  different files by runs.
"""

def readInput(fin):
    re1 = re.compile('(\d+)\s+(\d+)')
    m = {}
    for line in fin.readlines():
        mg = re1.search(line)
        if mg:
            run, event = int(mg.group(1)), int(mg.group(2))
            if m.has_key(run):
                m[run].append(event)
            else:
                m[run] = [event]
    return m

def writeOutput(m, prefix):
    keys = m.keys()
    keys.sort()
    for run in keys:
        events = m[run]
        fname_out = '%s_%08d.txt' % (prefix, run)
        print 'Create run/event file: %s' % fname_out
        fout = open(fname_out, 'w')
        for e in events:
            fout.write('%10d %10d\n' % (run, e))
        fout.close()
    pass

def main():
    if len(sys.argv) != 2:
        usage()
        status = 0
        if len(sys.argv) != 1: status = -1
        sys.exit(status)
    fname_in = sys.argv[1]
    if not os.path.exists(fname_in):
        sys.exit(-2)
    fin = open(fname_in, 'r')
    writeOutput(readInput(fin), fname_in.replace('.txt', ''))
    
if __name__ == '__main__':
    main()
    
