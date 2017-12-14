#!/usr/bin/env python
#------------------------------------------------------------------
# mk_tkwt (Make TK Webpage Template
#------------------------------------------------------------------

import sys, os
import getopt

def usage():
    print "Usage: %s" % (sys.argv[0])

#------------------------------------------------------------------
# Options
#------------------------------------------------------------------
filename=''
title=''
css_file=''
web_home=''

def get_options():
    global filename
    global title
    global css_file
    global web_home
    argv = sys.argv[1:]
    optlist, argv = getopt.getopt(argv, 't:c:h:',
                                  ['title', 'css_file', 'web_home'])
    print optlist
    print argv
    for opt, value in optlist:
        if opt == '-t': title = value
        if opt == '-c': css_file = value
        if opt == '_h': web_home = value
    if len(argv) > 1:
        print 'Too many arguments'
        return
    filename = argv[0]
    return

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        usage()
    get_options()
    if os.path.exists(filename):
        filename_bak = filename + '.bak'
        os.rename(filename, filename_bak)
        print "Warning: File %s exists. Renaming it to %s" % \
              (filename, filename_bak)
    file = open(filename, 'w')
    file.write('<html>\n\n')
    file.write('<title>\n')
    print 'title = ', title
    if title != '': file.write(title + '\n')
    else: file.write('\n')
    file.write('</title>\n\n')
    file.write('<body>\n\n')
    file.write('</body>\n\n') 
    file.write('</html>\n\n')
