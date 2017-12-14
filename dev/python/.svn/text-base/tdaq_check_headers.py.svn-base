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

def srcIdToInt(x):
    src_id = int(repr(x.subdetector_id()))
    module_id = int(repr(x.module_id()))
    return (src_id << 16) + module_id
def print_event_info(x):
    na = '--------'
    print 'EVENT         :          %08s %08s' % \
          (str(x.run_no().number()), str(x.lvl1_id()))
def print_subdet_info(x):
    na = '--------'
    print '  SUBDET      : %08x %08s %08s' % \
          (srcIdToInt(x.source_id()), na, na)
    return
def print_ros_info(x):
    print '    ROS       : %08x %08s %08s' % \
          (srcIdToInt(x.source_id()), str(x.run_no().number()),
           str(x.lvl1_id()))
def print_rob_info(x):
    na = '--------'
    print '      ROB     : %08x %08s %08s' % (srcIdToInt(x.source_id()),
                                              na, na)
    print '        ROD   : %08x %08s %08s' % \
          (srcIdToInt(x.rod_source_id()), str(x.rod_run_no().number()),
           str(x.rod_lvl1_id()))
    
nevents = -1
input_file = ''

if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()

if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'nevents = ', nevents
print 'input_file = ', input_file

input = EventApps.istream(input_file)

l1id=0
l1id_prev=-1

ievent = 0
for event in input:
    l1id = int(str(event.lvl1_id()))
    if l1id <= l1id_prev:
        print 'Error: l1id smaller than previos event, ', l1id
    print_event_info(event)
    for subdet in event.children():
        print_subdet_info(subdet)
        for ros in subdet.children():
            print_ros_info(ros)
            for rob in ros.children():
                print_rob_info(rob)
    l1id_prev = l1id
    print 'l1id: ', l1id
    
  
