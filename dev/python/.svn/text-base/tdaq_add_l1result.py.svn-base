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
filter_empty_roi = True

SubDet2Modify = [
  EventApps.TDAQ_CTP,
  EventApps.TDAQ_MUON_CTP_INTERFACE
  ]

SubDet2Remove = []
#  #EventApps.TILECAL_BARREL_A_SIDE, 
#  #EventApps.TILECAL_BARREL_C_SIDE
#  ]


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

ne_tot=0
ne_roi=0

for event in input:
  new_event = EventApps.write.FullEventFragment()
  cp_event_header(new_event, event)
  l2_subdet = EventApps.write.SubDetectorFragment()
  l2_subdet.source_id(EventApps.TDAQ_LVL2 <<16)
  l2_ros = EventApps.write.ROSFragment()
  l2_subdet.append(l2_ros)
  new_event.append(l2_subdet)
  n_muonroi = 0
  if l1id_out >= 0:
    new_event.lvl1_id(l1id_out)
    l2_ros.lvl1_id(l1id_out)
  for subdet in event.children():
    if subdet.source_id().subdetector_id() in SubDet2Remove:
      continue
    if subdet.source_id().subdetector_id() not in SubDet2Modify:
      new_event.append(EventApps.write.SubDetectorFragment(subdet))
      if l1id_out >= 0:
        for ros in subdet.children():
          ros.lvl1_id(l1id_out)
          for rob in ros.children():
            rob.rod_lvl1_id(l1id_out)
    else:
      new_event.append(EventApps.write.SubDetectorFragment(subdet))
      if l1id_out >= 0:
        for ros in subdet.children():
          ros.lvl1_id(l1id_out)
          for rob in ros.children():
            rob.rod_lvl1_id(l1id_out)
      #
      #new_subdet = EventApps.write.SubDetectorFragment()
      #new_event.append(new_subdet)
      #cp_subdet_header(new_subdet, subdet)
      for ros in subdet.children():
        cp_ros_header(l2_ros, ros)
        l2_ros.source_id(EventApps.TDAQ_LVL2 << 16)
        #
        #new_ros = EventApps.write.ROSFragment()
        #new_subdet.append(new_ros)
        #cp_ros_header(new_ros, ros)
        for rob in ros.children():
          #new_ros.append(EventApps.write.ROBFragment(rob))
          # Create a new ROB fragment.
          subdet_id = rob.source_id().subdetector_id()
          if subdet_id==EventApps.TDAQ_MUON_CTP_INTERFACE:
            # Create MUON_CTP_INTERFACE ROB under TDAQ_LVL2 ROS
            rod = rob.rod_source_id()
            roddata = rob.rod_data()
            roddata2 = []
            if len(roddata) != 0:
              muonroi_rob = EventApps.write.ROBFragment()
              cp_rob_header(muonroi_rob, rob)
              new_id = rob.source_id().code()+1
              muonroi_rob.source_id(new_id)
              muonroi_rob.rod_source_id(new_id)
              for (i, a) in enumerate(roddata):
                if i==0: continue
                #print '%08x: %08x -> %08x' % (i, a, convertMuonRoIWord(a))
                roddata2.append(convertMuonRoIWord(a))
              muonroi_rob.rod_data(roddata2)
              n_muonroi = len(roddata2)
              #new_ros.append(muonroi_rob)
              l2_ros.append(muonroi_rob)
          elif subdet_id==EventApps.TDAQ_CTP:
            # Create CTP ROB under TDAQ_LVL2 ROS
            ctp_rob = EventApps.write.ROBFragment()
            cp_rob_header(ctp_rob, rob)
            new_id = rob.source_id().code()+1
            ctp_rob.source_id(new_id)
            ctp_rob.rod_source_id(new_id)
            #
            ctp_roddata = rob.rod_data()
            roddata2 = []
            #
            n2 = len(ctp_roddata)
            if n2>0: roddata2.append(ctp_roddata[0])
            if n2>1: roddata2.append(ctp_roddata[1])
            for i in range(30):
              # roddata2.append(ctp_roddata[122+i])
              if n2>(302+i): roddata2.append(ctp_roddata[302+i])
            #
            # ctp_rob.rod_data(toSimpleList(rob.rod_data()))
            ctp_rob.rod_data(roddata2)
            #new_ros.append(ctp_rob)
            l2_ros.append(ctp_rob)
  #
  ievent += 1
  if l1id_out>0:
    l1id_out += 1
  ne_tot += 1
  if filter_empty_roi and n_muonroi==0:
    continue
  ne_roi += 1
  output.write(new_event)
  if ievent == nevents: break

print 'Wrote %d events in %s' % (output.events_in_file(),
                                 output.current_filename())

print 'N(with RoI)/N(total) = %d/%d' % (ne_roi, ne_tot)

sys.exit(0)
