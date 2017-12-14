#!/usr/bin/env python
#-------------------------------------------------------------------------
# Create a LVL1 result fragment sent from the LVL1 system to LVL2
# using the LVL1 DAQ data.
#-------------------------------------------------------------------------
import sys
import EventApps
from tdaq_tools import *

def usage():
  print 'usage: %s <input-file> <nevents> <First_Lvl1Id>=-1' % sys.argv[0]
  sys.exit(1)

nevents = -1
input_file = ''
l1id0 = -1

SubDet2Modify = [
  EventApps.TDAQ_CTP,
  EventApps.TDAQ_MUON_CTP_INTERFACE
  ]

SubDet2Remove = [
  EventApps.TILECAL_BARREL_A_SIDE, 
  EventApps.TILECAL_BARREL_C_SIDE,
  EventApps.TILECAL_EXT_A_SIDE, 
  EventApps.TILECAL_EXT_C_SIDE,
  EventApps.LAR_EM_BARREL_A_SIDE, 
  EventApps.LAR_EM_BARREL_C_SIDE,
  EventApps.LAR_EM_ENDCAP_A_SIDE, 
  EventApps.LAR_EM_ENDCAP_C_SIDE,
  EventApps.MUON_MDT_BARREL_A_SIDE, 
  EventApps.MUON_MDT_BARREL_C_SIDE, 
  EventApps.MUON_MDT_ENDCAP_A_SIDE, 
  EventApps.MUON_MDT_ENDCAP_C_SIDE, 
  ]


if len(sys.argv) not in [ 2, 3, 4 ]:
  usage()


if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])
if len(sys.argv)>3: l1id0 = int(sys.argv[3])

print 'nevents = ', nevents
print 'input_file = ', input_file


input = EventApps.istream(input_file)
output = EventApps.ostream() #we use the default output file

ievent = 0
l1id_out = -1
if l1id0 >= 0:
  l1id_out = l1id0

for event in input:
  new_event = EventApps.write.FullEventFragment()
  cp_event_header(new_event, event)
  l2_subdet = EventApps.write.SubDetectorFragment()
  l2_subdet.source_id(EventApps.TDAQ_LVL2 <<16)
  l2_ros = EventApps.write.ROSFragment()
  l2_subdet.append(l2_ros)
  new_event.append(l2_subdet)
  if l1id_out >= 0:
    new_event.lvl1_id(l1id_out)
    l2_ros.lvl1_id(l1id_out)
  for subdet in event.children():
    if subdet.source_id().subdetector_id() in SubDet2Remove:
      continue
    else:
      new_event.append(EventApps.write.SubDetectorFragment(subdet))
  #
  l1id_out += 1
  output.write(new_event)
  ievent += 1
  if ievent == nevents: break

print 'Wrote %d events in %s' % (output.events_in_file(),
                                 output.current_filename())
sys.exit(0)
