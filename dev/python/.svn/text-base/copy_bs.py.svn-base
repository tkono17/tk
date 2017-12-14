#!/usr/bin/env python


import sys
import EventApps
from mytools import *

def usage():
  print 'usage: %s <input-file> <input_file2>' % sys.argv[0]
  sys.exit(1)

if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()

nevents = -1
input_file = ''
input_file2 = ''

if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'nevents = ', nevents
print 'input_file = ', input_file


input = EventApps.istream(input_file)
output = EventApps.ostream() #we use the default output file

ievent = 0
for event in input:
  event0 = EventApps.write.FullEventFragment()
  print 'create event'
  cp_event_header(event0, event)
  print 'go'
  for subdet in event.children():
    print 'hi'
    subdet0 = EventApps.write.SubDetectorFragment()
    print 'create subdet'
    cp_subdet_header(subdet0, subdet)
    event0.append(subdet0)
    for ros in subdet.children():
      ros0 = EventApps.write.ROSFragment()
      print 'create ros'
      cp_ros_header(ros0, ros)
      subdet0.append(ros0)
      for rob in ros.children():
        rob0 = EventApps.write.ROBFragment()
        print 'create rob'
        cp_rob_header(rob0, rob)
        ros0.append(rob0)
  output.write(event0)

print 'done'

