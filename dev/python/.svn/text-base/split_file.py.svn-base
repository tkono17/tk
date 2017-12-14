#!/usr/bin/env python

import os, sys
import optparse

def createParser():
    parser = optparse.OptionParser()
    parser.add_option('-n', '--nLinesPerFile', action='store',
                      dest='nLinesPerFile', type='int', default='10')
    parser.add_option('-f', '--fileInput', action='store',
                      dest='fileInput', type='string', default='',
                      help='Default output files are named <prefix>_$i.<suffix> where input file name is interpreted as <prefix>.<suffix>')
    parser.add_option('-p', '--prefix', action='store',
                      dest='prefix', type='string', default='',
                      help='Change the prefix of output files')
    parser.add_option('-s', '--suffix', action='store',
                      dest='suffix', type='string', default='', 
                      help='Change the suffix of output files')
    parser.add_option('--no-comments', action='store_true',
                      dest='no_comments', default=False, 
                      help='Suppress comment lines like # (XXX entries)')
    return parser

def writeToFile(lines, ifile, prefix):
    fname = '%s_%d.txt' % (prefix, ifile)
    #print 'Writing %d lines to file: %s' % (len(lines), fname)
    f = open(fname, 'w')
    for line in lines:
        f.write('%s\n' % line)
    f.close()
    return fname
    
def readFileName(fname0):
    prefix, suffix = '', ''
    fname = os.path.basename(fname0)
    print 'FILE: %s' % fname
    idot = fname.rfind('.')
    if idot >= 0:
        prefix = fname[0:idot]
        suffix = fname[idot:-1]
    return prefix, suffix

def splitFile(fname_in, nlines_per_file, prefix, suffix, no_comments=False):
    n, n2 = 0, 0 # n: number of lines, n2: number of lines between comments
    ifile = 0
    nfiles = 0
    lines = []
    comments = []
    fnames = []
    f = open(fname_in, 'r')
    for line in f.readlines():
        if len(line)>0: line = line[:-1]
        if len(line)>0 and line[0] == '#': # comment
            if n2 > 0:
                comments.append('# (%d entries)' % n2)
                n2 = 0
            comments.append(line)
            pass
        elif len(line)>0:
            n += 1
            n2 += 1
        lines.append(line)
        if n != 0 and (n%nlines_per_file) == 0:
            fnames.append(writeToFile(lines, ifile, prefix))
            nfiles += 1
            comments.append('# (%d entries)' % n2)
            ifile += 1
            n, n2 = 0, 0
            if not no_comments:
                lines = list(comments)
            else:
                lines = []
    if len(lines)>0 and n!=0:
        fnames.append(writeToFile(lines, ifile, prefix))
        nfiles += 1
    return fnames

if __name__ == '__main__':
    parser = createParser()
    (options, args) = parser.parse_args()
    if options.fileInput == '':
        parser.print_help()
        sys.exit(1)
    fname_in = options.fileInput
    if not os.path.exists(fname_in):
        print 'Error: File %s does not exist' % fname_in
        sys.exit(2)

    # Optional parameters
    prefix, suffix = readFileName(fname_in)
    if options.prefix != '': prefix = options.prefix
    if options.suffix != '': suffix = options.suffix
    nlines_per_file = options.nLinesPerFile

    splitFile(fname_in, nlines_per_file, prefix, suffix, options.no_comments)
    
