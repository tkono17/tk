#!/usr/bin/env python

import os, sys
import re

def usage():
    print 'Usage: %s <output_from_list_dcache>' % sys.argv[0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    if os.path.exists(sys.argv[1]):
        n_datasets = 0
        n_empty_datasets = 0
        n_files = 0
        n_bytes = 0
        re0 = re.compile('([\S]+) => (.*) files, (.*) B')
        f = open(sys.argv[1], 'r')
        for line in f.readlines():
            if len(line) > 0: line = line[:-1]
            mg = re0.search(line)
            if mg:
                n_datasets += 1
                n1, n2 = 0, 0
                if mg.group(2) != '': n1 = int(mg.group(2))
                if mg.group(3) != '': n2 = int(mg.group(3))
                n_files += n1
                n_bytes += n2
                if n1 == 0 and n2 == 0:
                    n_empty_datasets += 1
                #print 'MG = ', mg.groups()
        print 'Number of datasets (empty): %d (%d)' % \
              (n_datasets, n_empty_datasets)
        print 'Number of files           : %d' % n_files
        print 'Total size (GB)           : %1.2f' % (n_bytes/1E+9)
        
