#!/usr/bin/env python

import os, sys

files = sys.argv[1].replace(',', ' ')
events = ''
f = open('event.txt', 'r')
for line in f.readlines():
    events += '%s,' % line.split()[-1]
events = events[:-1]
cmd = 'AtlCopyBSEvent.exe -e %s -o event.dat %s' % (events, files)
print cmd
status = os.system(cmd)
sys.exit(status % 255)
