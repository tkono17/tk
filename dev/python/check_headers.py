#!/usr/bin/env python
#-------------------------------------------------------------------------
# Check the information in the header of data fragments
# - Run no
# - Event no
# - Lvl1 ID
# - BC ID
# - 
#-------------------------------------------------------------------------
import sys
import EventApps
from tdaq_tools import *

def usage():
    print 'usage: %s <bytestream-file>' % sys.argv[0]
    sys.exit(1)

def print_event_info(x):
    print 'EVENT :          %08x %08x' % (x.run_no(), x.lvl1_id())
def print_subdet_info(x):
    print 'SUBDET: %08x %08x %08x' %
    (x.source_id().subdetector_id(), x.run_no(), x.lvl1_id())
def print_ros_info(x):
    print 'ROS   : %08x %08x %08x' % 
    (x.source_id().subdetector_id(), x.run_no(), x.lvl1_id())
def print_rob_info(x):
    print 'ROB   : %08x %08x %08x' % 
    (x.source_id().subdetector_id(), x.run_no(), x.lvl1_id())
    
nevents = -1
input_file = ''

if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()

if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'nevents = ', nevents
print 'input_file = ', input_file

input = EventApps.istream(input_file)

ievent = 0
for event in input:
    print_event_info(event)
    for subdet in event.children():
        print_subdet_info(subdet)
        for ros in subdet.children():
            print_ros_info(ros)
            for rob in ros.children():
                print_rob_info(rob)

  
