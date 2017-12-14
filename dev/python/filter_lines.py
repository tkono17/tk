#!/usr/bin/env python

import os
import sys
import getopt

def usage():
    print 'This script filters out or saves the lines in <file1> according to'
    print 'the lines specified in <file2>'
    print 'Usage: filter_lines.py [options] <file1> <file2>'
    print '------'
    print '<file1>: Input file to read'
    print '<file2>: A file containing lines to check for filtering/matching'
    print 'Options: -m :Save matched lines instead of filtering them out'

    
if __name__=='__main__':
    use_matched = False
    #---------------------------------------------------------------
    optval, args = getopt.getopt(sys.argv[1:], 'm')
    if len(args)!=2:
        usage()
        sys.exit(0)
    fname_in = args[0]
    fname_filter = args[1]
    for a in optval:
        if a[0]=='-m':
            use_matched=True
    #---------------------------------------------------------------
    f_filter = open(fname_filter, 'r')
    filter = []
    for line in f_filter.readlines():
        line = line[:-1]
        line = line.strip()
        if len(line)>0 and line[0]!='#':
            filter.append(line)
    f_filter.close()
    f_in = open(fname_in, 'r')
    for line in f_in.readlines():
        line = line[:-1]
        tmp = line.strip()
        if len(line)>0 and line[0]!='#':
            if use_matched and tmp in filter:
                print line
            elif not use_matched and (tmp not in filter):
                print line
        else:
            print line
    f_in.close()

