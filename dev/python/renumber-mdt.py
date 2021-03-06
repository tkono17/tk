#!/usr/bin/env python
# $Id: renumber-mdt.py 94762 2012-07-18 09:37:30Z tkohno $
# Created by Andre DOS ANJOS <Andre.dos.Anjos@cern.ch>, 08-Dec-2006

# Renumbers the ROB and ROD fragments in the LVL2 ROS (pROS)

import sys

if len(sys.argv) == 1 or len(sys.argv) > 3:
  print 'Replaces the source identifier of ROBs and ROD fragments'
  print 'produced in the L2PU, with the one given as input parameter.'
  print 'If no id is given, the default value of 0x%x is used.' % id
  print 'usage: %s <input-file> [id]' % sys.argv[0]
  sys.exit(1)

nevents = -1
if len(sys.argv) == 3:
  nevents = int(sys.argv[2])
  # id = long(sys.argv[2])

import EventApps

input = EventApps.istream([sys.argv[1]])
output = EventApps.ostream() #we use the default output file

mdt_src_ids = [
  EventApps.MUON_MDT_BARREL_A_SIDE,
  EventApps.MUON_MDT_BARREL_C_SIDE,
  EventApps.MUON_MDT_ENDCAP_A_SIDE,
  EventApps.MUON_MDT_ENDCAP_C_SIDE
  ]

ievent = 0
for event in input:
  for subdet in event.children():
    for ros in subdet.children():
      if ros.source_id().subdetector_id() in mdt_src_ids:
        for rob in ros.children():
          rod_id = rob.rod_source_id().code()
          rob_id = rob.source_id().code()
          rob.source_id(rob.rod_source_id())
          # print 'MDT ROB: %08x ROD: %08x' % (rod_id, rob_id)
  output.write(event)
  ievent += 1
  if ievent == nevents: break

print 'Wrote %d events in %s' % (output.events_in_file(),
                                 output.current_filename())
sys.exit(0)
