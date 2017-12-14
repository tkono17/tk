#!/usr/bin/env python

import os, sys
import optparse
import subprocess

def parseOptions():
    op = optparse.OptionParser()
    op.add_option('-m', '--macro-name', dest='macro_name',
                  action='store', default='',
                  help='ROOT macro name (mandatory)')
    op.add_option('--no-b', dest='no_b', action='store_false', default=False, 
                  help="Do not use '-b' option when calling ROOT")
    op.add_option('--no-q', dest='no_q', action='store_false', default=False, 
                  help="Do not use '-q' option when calling ROOT")
    return op.parse_args()

def is_int(x):
    try:
        b = int(x)
    except:
        return False
    return True

def is_float(x):
    try:
        b = float(x)
    except:
        return False
    return True

if __name__ == '__main__':
    (options, args) = parseOptions()
    if options.macro_name == '': sys.exit(1)
    print 'options = ', options
    print 'args = ', args
    
    cmd = 'root -l'
    if not options.no_b: cmd += ' -b'
    if not options.no_q: cmd += ' -q'
    cmd += ' %s+' % options.macro_name

    if len(sys.argv) > 1: cmd += '('
    for i, arg in enumerate(args):
        tmp = ''
        if i > 0: tmp = ','
        if is_int(arg) or is_float(arg):
            cmd += '%s%s' % (tmp, arg)
        else:
            cmd += '%s"%s"' % (tmp, arg)
    if len(sys.argv) > 1: cmd += ')'
    print "Execute command='%s'" % cmd

    
