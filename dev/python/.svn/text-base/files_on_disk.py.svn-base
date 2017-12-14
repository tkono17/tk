#!/usr/bin/env python

import os
import getopt
import sys
import re

def usage():
    print 'Usage: files_on_disk.py [options]'
    print '------'
    print 'Options: -r <root_dir>'
    print '         -d <directory_name>'
    print '         -f <filename>'
    print '         -s'


if __name__=='__main__':
    root_dir=''
    dir_name=''
    filename=''
    save_listing=False
    from_file = False
    #
    #--------------------------------------------------------------
    # Interprete arguments
    optval, args = getopt.getopt(sys.argv[1:], 'r:d:f:s')
    for a in optval:
        if a[0]=='-r':
            root_dir = a[1].rstrip('/')
        elif a[0]=='-d':
            dir_name = a[1].rstrip('/')
        elif a[0]=='-f':
            filename = a[1]
            from_file = True
        elif a[0]=='-s':
            save_listing = True
    if dir_name=='' and not from_file:
        usage()
        sys.exit(0)
    #--------------------------------------------------------------
    dirs = []
    if from_file:
        f = open(filename, 'r')
        for line in f.readlines():
            line = line[:-1]
            line = line.strip()
            if len(line)==0 or line[0]=='#': continue
            dirs.append(line)
        f.close()
    else:
        dirs = dataset
    print 'N : ', len(dirs)
    max_name = 0
    for dir in dirs:
        if len(dir) > max_name: max_name = len(dir)
        
    for dir in dirs:
        list2 = os.listdir(root_dir+os.sep+dir)
        listing = []
        re_dir = re.compile(dir)
        for a in list2:
            fullpath = os.path.join(root_dir, dir, a)
            if os.path.isfile(fullpath) and re_dir.search(a)!=None:
                listing.append(a)
        n = len(listing)
        format_string = "%%%ds : %%d" % max_name
        print format_string % (dir, n)
        if save_listing:
            out_name = "%s_disk.txt" % (dir)
            out_name = out_name.replace('/', '_')
            f = open(out_name, 'w')
            if listing!=None:
                for a in listing:
                    f.write(a+'\n')
            f.close()
