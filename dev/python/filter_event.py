#!/usr/bin/env python
# $Id: filter_event.py 94762 2012-07-18 09:37:30Z tkohno $
# Created by Andre DOS ANJOS <Andre.dos.Anjos@cern.ch>, 08-Dec-2006

# Renumbers the ROB and ROD fragments in the LVL2 ROS (pROS)

import sys
import EventApps

if len(sys.argv) == 1 or len(sys.argv) > 3:
  print 'Replaces the source identifier of ROBs and ROD fragments'
  print 'produced in the L2PU, with the one given as input parameter.'
  print 'If no id is given, the default value of 0x%x is used.' % id
  print 'usage: %s <input-file> [id]' % sys.argv[0]
  sys.exit(1)

if len(sys.argv) == 3:
  id = long(sys.argv[2])


input = EventApps.istream([sys.argv[1]])
#output = EventApps.ostream() #we use the default output file
#replacement = EventApps.SourceIdentifier(id)

ros_to_save = [
  EventApps.MUON_ANCILLARY_CRATE, 
  EventApps.MUON_MDT_BARREL_A_SIDE, 
  EventApps.MUON_MDT_BARREL_C_SIDE, 
  EventApps.MUON_MDT_ENDCAP_A_SIDE, 
  EventApps.MUON_MDT_ENDCAP_C_SIDE, 
  EventApps.MUON_RPC_BARREL_A_SIDE, 
  EventApps.MUON_RPC_BARREL_C_SIDE, 
  EventApps.MUON_TGC_ENDCAP_A_SIDE, 
  EventApps.MUON_TGC_ENDCAP_C_SIDE, 
  EventApps.MUON_CSC_ENDCAP_A_SIDE, 
  EventApps.MUON_CSC_ENDCAP_C_SIDE, 
  EventApps.TDAQ_BEAM_CRATE, 
  EventApps.TDAQ_CALO_PREPROC, 
  EventApps.TDAQ_CALO_CLUSTER_PROC_DAQ,
  EventApps.TDAQ_CALO_CLUSTER_PROC_ROI, 
  EventApps.TDAQ_CALO_JET_PROC_DAQ, 
  EventApps.TDAQ_CALO_JET_PROC_ROI, 
  EventApps.TDAQ_MUON_CTP_INTERFACE, 
  EventApps.TDAQ_CTP, 
  EventApps.TDAQ_L2SV, 
  EventApps.TDAQ_LVL2, 
  EventApps.TDAQ_EVENT_FILTER 
  ]

nevents = 100
ievent = 0
for event in input:
  for subdet in event.children():
    for ros in subdet.children():
      if ros.source_id().subdetector_id() in ros_to_save or True:
        for rob in ros.children():
          rod = rob.rod_source_id()
          print 'ROS/ROB/ROD : %04x%04x %04x%04x %04x%04x' % \
                (ros.source_id().subdetector_id(),
                 ros.source_id().module_id(), 
                 rob.source_id().subdetector_id(),
                 rob.source_id().module_id(), 
                 rod.subdetector_id(),
                 rod.module_id())
  # output.write(event)
  ievent += 1
  if ievent == nevents: break

#print 'Wrote %d events in %s' % (output.events_in_file(),
#                                 output.current_filename())
sys.exit(0)
