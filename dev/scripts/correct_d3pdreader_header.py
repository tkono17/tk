#!/usr/bin/env python

import os, sys
import re
import optparse

def parse_args():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='input', default='', action='store',
                      help='Input file')
    parser.add_option('-o', '--output',
                      dest='output', default='', action='store',
                      help='Output file')
    parser.add_option('-p', '--header-path',
                      dest='header_path', default='', action='store',
                      help='Header path')
    #
    parser.add_option('--source-directory',
                      dest='source_directory', default='', action='store', 
                      help='Source directory. Use it to process multiple files at once')
    parser.add_option('--src-dest',
                      dest='src_dest', default='', action='store',
                      help='Source destination. Use it to process multiple files at once')
    parser.add_option('--header-dest',
                      dest='header_dest', default='', action='store',
                      help='Header destination. Use it to process multiple files at once')
    return parser.parse_args()

def processFile(fname_in, fname_out, header_path):
    fin = open(fname_in, 'r')
    if fname_out == '':
        fout = sys.stdout
    else:
        fout = open(fname_out, 'w')

    re0 = re.compile('(^#include\s+"([\w_\/\.-]+)")')
    dir0 = os.path.dirname(fname_in)
    
    for line in fin.readlines():
        mg = re0.match(line)
        ok=False
        if mg:
            # print '%s: %s' % (fname_in, str(mg.groups()))
            hdr = mg.group(2)
            if os.path.exists(os.path.join(dir0, hdr)):
                hdr2 = os.path.join(header_path, hdr)
                # print 'hdr %s -> %s' % (hdr, hdr2)
                fout.write('#include "%s"\n' % hdr2)
                ok=True
        if not ok:
            fout.write(line)
    pass

if __name__ == '__main__':
    options, args = parse_args()

    if options.source_directory != '' and \
       options.src_dest != '' and options.header_dest != '':
        files = os.listdir(options.source_directory)
        srcs, headers = [], []
        for f in files:
            if f.endswith('.cxx'):
                srcs.append(f)
            elif f.endswith('.h') or f.endswith('.hxx') or f.endswith('.icc'):
                headers.append(f)
        for f in srcs:
            fbase = os.path.basename(f)
            out = os.path.join(options.src_dest, fbase)
            processFile(f, out, options.header_path)
        for f in headers:
            fbase = os.path.basename(f)
            out = os.path.join(options.header_dest, fbase)
            processFile(f, out, options.header_path)
    elif fname_in != '':
        fname_in = options.input
        fname_out = options.output
    else:
        print 'Invalid options'
        
                
    
