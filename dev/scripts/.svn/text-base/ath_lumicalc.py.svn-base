#!/usr/bin/env python

import os, sys
import re
import commands

prog = 'iLumiCalc.exe'
xmlfiles = [
    'a'
]

if __name__ == '__main__':
    s = ': SUMMARY ([^$]+) ([^$]+) ([^$]+) ([^$]+) ([^$]+) ([^$]+)'
    re1 = re.compile(s)
    for x in xmlfiles:
        # (status, output) = commands.getstatusoutput(command)
        f = open('lumi.txt', 'r')
        output = f.readlines()
        run, lb0, lb1, n, lumi0, lumi1 = 0, 0, 0, 0, 0, 0
        for line in output:
            mg = re1.search(line)
            if mg:
                run = int(mg.group(1))
                lb0 = int(mg.group(2))
                lb1 = int(mg.group(2))
                n = int(mg.group(2))
                lumi0 = float(mg.group(2))
                lumi1 = float(mg.group(2))
                print 'run=%d' % run
                
            
