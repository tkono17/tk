#!/usr/bin/env python

import os, sys
import re

def findList(pattern, lines):
    endpat = ']'
    for l in lines:
        mg = re.search(pattern, l)
        if mg:
            print 'line: ', l
            re.sub(pattern, 'tmp')
            

if __name__ == '__main__':
    fp = open('FDR2_lumi1E32.py', 'r')
    lines = fp.readlines()
    findList('TriggerFlags.Lvl1.thresholds', lines)
    findList('TriggerFlags.Lvl1.items', lines)

