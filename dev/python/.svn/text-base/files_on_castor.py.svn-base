#!/usr/bin/env python

import sys
import getopt
import castor_util

def usage():
    print 'Usage: files_on_castor.py [options]'
    print '------'
    print 'Options: -r <root_dir> (Root CASTOR directory to work with)'
    print '         -d <dir_name> (A base directory name under <root_dir>)'
    print '         -f <filename> (A file with list of dir_names under <root_dir>)'
    print '            This overwrites the -d option.'
    print '         -s (Save the list of files in each directory)'
    
if __name__=='__main__':
    root_dir=''
    filename=''
    dir_name=''
    output_file=''
    from_file=False
    save_listing=False
    #--------------------------------------------------------------
    # Interprete arguments
    optval, args = getopt.getopt(sys.argv[1:], 'r:f:d:s')
    for a in optval:
        # print a
        if a[0]=='-r':
            root_dir = a[1]
        elif a[0]=='-f':
            from_file = True
            filename = a[1]
        elif a[0]=='-d':
            dir_name=a[1]
        elif a[0]=='-o':
            output_file=a[1]
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
        dirs = dir_name
    print 'N : ', len(dirs)
    max_name = 0
    for dir in dirs:
        if len(dir) > max_name: max_name = len(dir)
        
    for dir in dirs:
        fullpath="%s/%s" % (root_dir, dir)
        listing = castor_util.castor_listdir(fullpath)
        n = -1
        if listing!=None:
            n = listing.getEntries()
        format_string = "%%%ds : %%d" % max_name
        print format_string % (dir, n)
        if save_listing:
            out_name = "%s_castor.txt" % (dir)
            out_name = out_name.replace('/', '_')
            f = open(out_name, 'w')
            if listing!=None:
                for a in listing.subs:
                    f.write(a.name+'\n')
            f.close()

