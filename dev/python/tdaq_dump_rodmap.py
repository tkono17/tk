#!/usr/bin/env python
#-------------------------------------------------------------------------
# Dump ROS/ROB mapping in a bytestream file
#-------------------------------------------------------------------------
import sys
import EventApps
from tdaq_tools import *

def usage():
  print 'usage: %s <input-file> <nevents> <First_Lvl1Id>=-1' % sys.argv[0]
  sys.exit(1)

nevents = -1
input_file = ''

if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()

if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'nevents = ', nevents
print 'input_file = ', input_file

input = EventApps.istream(input_file)

ros_rob_map = []

ievent = 0
for event in input:
  for subdet in event.children():
    if subdet.source_id().subdetector_id() in SubDet2Check:
      for ros in subdet.children():
        ros_id = ros.source_id().subdetector_id()<<16 +\
                 ros.source_id().module_id()
        for rob in ros.children():
          subdet_id = rob.source_id().subdetector_id()
          rob_id = rob.source_id().subdetector_id()<<16 +\
                   rob.source_id().module_id()
          if (ros_id, rob_id) not in ros_rob_map:
            ros_rob_map.append( (ros_id, rob_id))
##           if subdet_id==EventApps.TDAQ_MUON_CTP_INTERFACE:
##             print 'MUCTPI ROD size: ', len(rob.rod_data())
##           elif subdet_id==EventApps.TDAQ_CTP:
##             statusdata = rob.status()
##             print 'CTP ROB status:', len(statusdata)
##             istatus = 0
##             for istatus in range(len(statusdata)):
##               print 'CTP ROB status %d: %08x' % (istatus, statusdata[istatus])
##             roddata = rob.rod_data()
##             statusdata = rob.rod_status()
##             print 'CTP ROD size: ', len(roddata)
##             print 'CTP ROD status:', len(statusdata)
##             istatus = 0
##             for istatus in range(len(statusdata)):
##               print 'CTP ROD status %d: %08x' % (istatus, statusdata[istatus])
##             irod = 0
##             for irod in range(len(roddata)):
##               print 'CTP %2d: %08x' % (irod, roddata[irod])
  #
  ievent += 1
  if ievent == nevents: break

for (ros_id, rob_id) in ros_rob_map:
  print '%08x %08x' % (ros_id, rob_id)

sys.exit(0)
