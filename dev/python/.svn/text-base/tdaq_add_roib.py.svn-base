#!/usr/bin/env python
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Mon 20 Aug 2007 02:50:16 PM CEST 

# Copies the data in the TDAQ_CTP rob with identifier 0
# into a new TDAQ_LVL2 subdetector and renames it with
# TDAQ_CTP identifier 1 (to fake the existence of the 
# LVL1 result).

import sys

if len(sys.argv) == 1:
  print "Copies LVL1 ROS MUCTPI data to the TDAQ_LVL2 subdetector"
  print "legend:"
  print " . => Event had the LVL1 ROS MUCTPI data copied as RoIB MUCTPI"
  print " ! => The event was copied w/o modification (already has L2R)"
  print " x => Could not find the LVL2 ROS CTP data in the event"
  print "usage: %s <input-file>" % sys.argv[0]
  sys.exit(1)

def convertMuonRoIWord(word_in_muctpi_rod_data):
  """Convert the muon RoI word stored in the MUCTPI ROD data into the
  format used in the RoI word sent to LVL2"""
  daqData = word_in_muctpi_rod_data
  first = (daqData >> 25) & 0x1
  secAddress = (daqData >> 17) & 0xff
  lvl2Word = 0
  lvl2Word |= (first << 22);
  lvl2Word |= (secAddress << 14);
  lvl2Word |= (daqData & 0x1fff);
  # add one to RoI number
  lvl2Word |= (1<<2)
  return lvl2Word

import EventApps
out = EventApps.ostream()
istream = EventApps.istream(sys.argv[1])
sys.stdout.write("Processing %d events\n" % len(istream))
ievent=0
for e in istream:
  # if ievent == 10 : break
  ievent += 1
  
  contains_lvl2_result = False
  lvl2_muctpi_rob = None
  lvl2_ctp_rob = None
  for sd in e.children():
    if sd.source_id().subdetector_id() == EventApps.TDAQ_LVL2:
      contains_lvl2_result = True
      for ros in sd.children():
        for rob in ros.children():
          subdet_id = rob.source_id().subdetector_id()
          module_id = rob.source_id().module_id()
          if subdet_id == EventApps.TDAQ_CTP and \
                 module_id == 0x1:
            lvl2_ctp_rob = rob
          elif subdet_id == EventApps.TDAQ_MUON_CTP_INTERFACE and \
                   module_id == 0x1:
            lvl2_muctpi_rob = rob

  if contains_lvl2_result and lvl2_ctp_rob!=None and lvl2_muctpi_rob!=None:
    # This time overwrite MUCTPI ROB fragment in TDAQ_LVL2 ROS fragment
    #just copy the whole event.
    out.write(e)
    sys.stdout.write('!')
    sys.stdout.flush()
  else:
    #in this case, we try to look for the CTP rob
    ctp_rob = None
    muctpi_rob = None
    lvl2_ros = None
    new_event = EventApps.write.FullEventFragment(e)
    for sd in new_event.children():
      for ros in sd.children():
        ros_subdet_id=ros.source_id().subdetector_id()
        if ros_subdet_id==EventApps.TDAQ_LVL2:
          lvl2_ros = ros
        for rob in ros.children():
          subdet_id = rob.source_id().subdetector_id()
          module_id = rob.source_id().module_id()
          if ros_subdet_id==EventApps.TDAQ_CTP and \
             subdet_id == EventApps.TDAQ_CTP and module_id == 0:
            ctp_rob = rob
          elif ros_subdet_id==EventApps.TDAQ_MUON_CTP_INTERFACE and \
               subdet_id==EventApps.TDAQ_MUON_CTP_INTERFACE and module_id==0:
            muctpi_rob = rob
    #
    if lvl2_ros == None:
      lvl2_ros = EventApps.write.ROSFragment()
      lvl2_ros.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_LVL2, 0))
      lvl2_sd = EventApps.write.SubDetectorFragment()
      lvl2_sd.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_LVL2, 0))
      lvl2_sd.append(lvl2_ros)
      new_event.append(lvl2_sd)
      
##     if lvl2_muctpi_rob is None and muctpi_rob is None:
##       sys.stdout.write('x')
##       sys.stdout.flush()
##       continue

    # copy MUCTPI data words into the MUCTPI fragment in the LVL2 fragment.
    if not muctpi_rob is None and lvl2_muctpi_rob is None:
      lvl2_muctpi_rob = EventApps.write.ROBFragment()
      lvl2_muctpi_rob.copy_header(muctpi_rob)
      lvl2_muctpi_rob.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_MUON_CTP_INTERFACE, 1))
      if len(lvl2_muctpi_rob.rod_data())==0:
        roddata = muctpi_rob.rod_data()
        roddata2 = []
        for i in range(1, len(roddata)):
          roddata2.append(convertMuonRoIWord(roddata[i]))
        lvl2_muctpi_rob.rod_data(roddata2)
        lvl2_ros.append(lvl2_muctpi_rob)

    if not ctp_rob is None and lvl2_ctp_rob is None:
      lvl2_ctp_rob = EventApps.write.ROBFragment()
      lvl2_ctp_rob.copy_header(ctp_rob)
      lvl2_ctp_rob.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_CTP, 1))
      if len(lvl2_ctp_rob.rod_data())==0:
        roddata = ctp_rob.rod_data()
        roddata2 = []
        for i in range(0, 2):
          roddata2.append(roddata[i])
        for i in range(302, 332):
          roddata2.append(roddata[i])
        lvl2_ctp_rob.rod_data(roddata2)
      lvl2_ros.append(lvl2_ctp_rob)

    sys.stdout.write('.')
    sys.stdout.flush()
    out.write(new_event)
   
sys.stdout.write('\n')
sys.stdout.flush()
import os
rename_from = out.last_filename()
total = out.events_in_file()
del out # to close the output file
result = os.path.basename(sys.argv[1]) + '.withMuRoI'
os.rename(rename_from, result)
print "Saved file %s with %d events in it." % (result, total)
