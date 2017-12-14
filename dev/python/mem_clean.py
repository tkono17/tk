#!/usr/bin/env python

import sys

n = 20 # MB

if len(sys.argv)>1: n = int(sys.argv[1])

n *= 1000000
n /= 4 # words

a=[]
b = (n / 20)
for i in range(n):
    a.append( (i, i+1))
    if (i % b) == 0:
        sys.stdout.write('.')
        sys.stdout.flush()

