#!/usr/bin/env python

import os
import commands
import optparse

def createParser():
    usage = 'usage: %prog [options] <dataset_name>'
    parser = optparse.OptionParser(usage=usage)
    return parser

def erase_dataset(ds):
    if ds.endswith('/'):
        print 'Erase dataset container: %s' % ds
        v = find_sub_datasets(ds)
        # print 'v = ', v
        for d in v:
            erase_dataset(d)
        cmd = 'dq2-erase %s' % ds
        os.system(cmd)
    else:
        # cmd = 'dq2-erase %s' % ds
        cmd = 'dq2-delete-replicas %s --all' % ds
        # print cmd
        # status, output = commands.getstatusoutput(cmd)
        os.system(cmd)
        #if status != 0:
        #    print output

def find_sub_datasets(ds):
    cmd = 'dq2-list-datasets-container %s' % ds
    status, output = commands.getstatusoutput(cmd)
    v = []
    if status == 0:
        v = output.split(os.linesep)
    return v
               
if __name__ == '__main__':
    parser = createParser()
    (options, args) = parser.parse_args()
    if len(args) > 0:
        for d in args:
            erase_dataset(d)
