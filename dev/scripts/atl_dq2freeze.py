#!/usr/bin/env python

import os
import commands
import optparse

def createParser():
    usage = 'usage: %prog [options] <dataset_name>'
    parser = optparse.OptionParser(usage=usage)
    return parser

def freeze_dataset(ds):
    if ds.endswith('/'):
        print 'Freeze dataset container: %s' % ds
        v = find_sub_datasets(ds)
        # print 'v = ', v
        for d in v:
            freeze_dataset(d)
    else:
        cmd = 'dq2-freeze-dataset %s' % ds
        # print cmd
        # status, output = commands.getstatusoutput(cmd)
        os.system(cmd)
        #if status != 0:
        #    print output

def find_sub_datasets(ds):
    cmd = 'dq2-list-datasets-container %s' % ds
    output = commands.getoutput(cmd)
    return output.split(os.linesep)
##     cmd = 'dq2-ls -r %s' % ds
##     output = commands.getoutput(cmd)
##     ds1 = ds[:-1]
##     lines = output.split(os.linesep)
##     out = []
##     il = 0
##     while il < len(lines):
##         i = lines[il].find(ds1)
##         if i >= 0 and lines[il+1].find('INCOMPLETE') >= 0 and \
##                lines[il+2].find('COMPLETE') >= 0:
##             s = lines[il+1].replace('INCOMPLETE:', '').strip()
##             incomplete_data, complete_data = False, False
##             if len(s) > 0: incomplete_data = True
##             s = lines[il+2].replace('COMPLETE:', '').strip()
##             if len(s) > 0: complete_data = True
##             if incomplete_data:
##                 tmp = lines[il]
##                 out.append(tmp[:tmp.find(':')])
##             il += 3
##         else:
##             il += 1
##     return out
               
if __name__ == '__main__':
    parser = createParser()
    (options, args) = parser.parse_args()
    if len(args) > 0:
        for d in args:
            freeze_dataset(d)
