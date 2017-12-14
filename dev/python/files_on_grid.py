#!/usr/bin/env python

import os
import sys
import getopt



def usage():
    print 'Usage: files_on_grid.py [options]'
    print '------'
    print 'Options: -d <dataset> (Dataset name)'
    print '         -f <filename> (A file with a list of datasets)'
    print '         -s (Save list of files for each dataset into a file)'

    
if __name__=='__main__':
    dataset=''
    filename=''
    from_file=False
    save_listing = False
    #--------------------------------------------------------------
    # Interprete arguments
    optval, args = getopt.getopt(sys.argv[1:], 'd:f:s')
    for a in optval:
        if a[0]=='-d':
            dataset = a[1]
        elif a[0]=='-f':
            filename = a[1]
            from_file = True
        elif a[0]=='-s':
            save_listing = True
    if dataset=='' and not from_file:
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
        command = "dq2_ls -g %s" % dir
        print 'executing ... ', command
        listing = []
##         f = os.popen(command, 'r')
##         print 'done'
##         for line in f.readlines():
##             line = line[:-1]
##             print 'line = ', line
##             line = line.strip()
##             if len(line)==0 or line[0]=='#': continue
##             listing.append(line)
##         f.close()
        n = len(listing)
        format_string = "%%%ds : %%d" % max_name
        print format_string % (dir, n)
        if save_listing:
            out_name = "%s_grid.txt" % (dir)
            out_name = out_name.replace('/', '_')
            f = open(out_name, 'w')
            if listing!=None:
                for a in listing:
                    f.write(a+'\n')
            f.close()

    
            
