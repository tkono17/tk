#!/usr/bin/env python

import os,sys
import re

if len(sys.argv)>1: filename = sys.argv[1]
else:
    sys.exit(0)

comp_type = ''
type = ''
name = ''

re_svc = re.compile("Service\('([:\w]+)/(\w+)'\)")
re_algo = re.compile("Algorithm\('([:\w]+)/(\w+)'\)")
re_prop = re.compile('\s*(\w+)\.(\w+)\s*=\s*"(\w+)"\s*:\s*([\.\w\s",\[\]/:\-]+)')
file = open(filename, 'r')
for line in file.readlines():
    line = line[:-1]
    mg_svc = re_svc.match(line)
    if mg_svc:
        comp_type = 'SERVICE'
        name = mg_svc.group(2)
        type = name
        print '#'
        print "theApp.ExtSvc('" + type + '/' + name + "')"
        print name + ' = ' + "Service('" + type + '/' + name + "')"
    mg_algo = re_algo.match(line)
    if mg_algo:
        comp_type = 'ALGORITHM'
        type = mg_algo.group(1)
        name = mg_algo.group(2)
        print '#'
        print name + ' = ' + "Algorithm('" + type + '/' + name + "')"
    mg = re_prop.match(line)
    if mg:
        comp_name = mg.group(1)
        prop_name = mg.group(2)
        prop_name2 = mg.group(3)
        prop_value = mg.group(4)
        if comp_name!=name:
            print 'WARNING!!! Component of ',comp_name, \
                  ' previously found to be ', name
        if prop_name!=prop_name2:
            print 'WARNING!!! Two property names differ!,', line
        print comp_name+'.'+prop_name+' = '+prop_value

    
