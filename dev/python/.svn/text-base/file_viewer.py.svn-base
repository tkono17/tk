#!/usr/bin/env python
import sys
import struct
def rd_binary_file(filename, nbyte):
    myfile = open(filename, 'rb')
    null_string = ''
    line = ''
    x = myfile.read(4)
    nword_in_line = 0
    while x != null_string:
        if nword_in_line == 7:
            print line+'END'
            nword_in_line = 0
            line = ''
        else:
            if nword_in_line == 0:
                line = "%s" % (x)
            else:
                line = "%s %s" % (line, x)
            nword_in_line = nword_in_line+ 1
        x = myfile.read(4)
    if line != null_string:
        print line
    return
filename = 'hallo'
nbyte = 1
if len(sys.argv) > 1: filename = sys.argv[1]
if len(sys.argv) > 2: nbyte = sys.argv[2]
print 'filename = ', filename
print 'nbyte = ', nbyte
rd_binary_file(filename, nbyte)
