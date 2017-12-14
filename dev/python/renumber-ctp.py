#!/usr/bin/env python
# $Id: renumber-ctp.py 94762 2012-07-18 09:37:30Z tkohno $
# Created by Andre DOS ANJOS <Andre.dos.Anjos@cern.ch>, 08-Dec-2006

# Renumbers the ROB and ROD fragments in the LVL2 ROS (pROS)

import sys
id = 0x770001

if len(sys.argv) == 1 or len(sys.argv) > 3:
  print 'Replaces the source identifier of ROBs and ROD fragments'
  print 'produced in the L2PU, with the one given as input parameter.'
  print 'If no id is given, the default value of 0x%x is used.' % id
  print 'usage: %s <input-file> [id]' % sys.argv[0]
  sys.exit(1)

if len(sys.argv) == 3:
  id = long(sys.argv[2])

import EventApps

input = EventApps.istream([sys.argv[1]])
output = EventApps.ostream() #we use the default output file
replacement = EventApps.SourceIdentifier(id)

nevents = 100
ievent = 0
for event in input:
  for subdet in event.children():
    for ros in subdet.children():
      if ros.source_id().subdetector_id() == EventApps.TDAQ_LVL2:
      # if ros.source_id().subdetector_id() == EventApps.TDAQ_CTP:
        for rob in ros.children():
          if rob.source_id().subdetector_id() == EventApps.TDAQ_CTP and \
                 (rob.source_id().code()&0x1) == 0:
            rob.source_id(replacement)
            rob.rod_source_id(replacement)
  output.write(event)
  ievent += 1
  if ievent == nevents: break

print 'Wrote %d events in %s' % (output.events_in_file(),
                                 output.current_filename())
sys.exit(0)
