#!/usr/bin/python2.2
import os
import re

re_root = re.compile(r'root')
re_rootexe = re.compile(r'root.exe')

os.system('ps -u kohno>tmp')
f = open('tmp', 'r')
for a in f.readlines():
    if re_rootexe.search(a):
        b = a.split()
        command = "kill -9 %s" % b[0]
        os.system(command)
        print 'Killed process ', b[0]
for a in f.readlines():
    b = a.split()
    if (not re_rootexe.search(a) and re_root.search(a)) \
           or b[3]=='root':
        command = "kill -9 %s" % b[0]
        os.system(command)
        print 'Killed process ', b[0]
os.system('rm tmp')
