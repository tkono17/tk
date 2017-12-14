#!/usr/bin/env python
#-------------------------------------------------------------------------
# Create a LVL1 result fragment sent from the LVL1 system to LVL2
# using the LVL1 DAQ data.
#-------------------------------------------------------------------------

import sys
import EventApps

def usage():
  print 'usage: %s <input-file> <input_file2>' % sys.argv[0]
  sys.exit(1)

if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()

nevents = -1
input_file = ''

if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'nevents = ', nevents
print 'input_file = ', input_file

input = EventApps.istream(input_file)

# output = EventApps.ostream() #we use the default output file

print 'TDAQ_LVL2: %08x' % EventApps.TDAQ_LVL2

ievent = 0
for event in input:
  for subdet in event.children():
    for ros in subdet.children():
      print 'ROS: subdet=%08x module=%08x' % (ros.source_id().subdetector_id(),
                                              ros.source_id().module_id())
      for rob in ros.children():
        rod = rob.rod_source_id()
        print 'ROS/ROB/ROD : %04x%04x %04x%04x %04x%04x' % \
              (ros.source_id().subdetector_id(),
               ros.source_id().module_id(), 
               rob.source_id().subdetector_id(),
               rob.source_id().module_id(), 
               rod.subdetector_id(),
               rod.module_id())
        print 'Payload size: %d' % rob.payload_size_word()
        roddata = rob.rod_data()
        print 'ROD data size: %d' % len(roddata)
        for (i, a) in enumerate(roddata):
          print 'ROD data [%04d]: %08x' % (i, a)
  ievent += 1
  if ievent == nevents: break

sys.exit(0)
