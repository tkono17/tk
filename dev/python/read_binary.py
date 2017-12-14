#!/usr/bin/env python

f = open('blocktest.dat', 'rb')

while True:
    s = f.read(8)
    for x in s:
        print '%x ' % x

