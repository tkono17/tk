#!/usr/bin/env python
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Mon 20 Aug 2007 02:50:16 PM CEST 

# Copies the data in the TDAQ_CTP rob with identifier 0
# into a new TDAQ_LVL2 subdetector and renames it with
# TDAQ_CTP identifier 1 (to fake the existence of the 
# LVL1 result).

import sys

if len(sys.argv) == 1:
  print "Copies LVL1 ROS CTP data to the TDAQ_LVL2 subdetector"
  print "legend:"
  print " . => Event had the LVL1 ROS CTP data copied as RoIB CTP"
  print " ! => The event was copied w/o modification (already has L2R)"
  print " x => Could not find the LVL2 ROS CTP data in the event"
  print "usage: %s <input-file>" % sys.argv[0]
  sys.exit(1)

import EventApps
out = EventApps.ostream()
istream = EventApps.istream(sys.argv[1])
sys.stdout.write("Processing %d events" % len(istream))
for e in istream: 
  contains_lvl2_result = False
  for sd in e.children():
    if sd.source_id().subdetector_id() == EventApps.TDAQ_LVL2:
      contains_lvl2_result = True

  if contains_lvl2_result:
    #just copy the whole event.
    out.write(e)
    sys.stdout.write('!')
    sys.stdout.flush()
    
  else:
    #in this case, we try to look for the CTP rob
    ctp_rob = None
    ctp_ros = None
    for sd in e.children():
      for ros in sd.children():
        for rob in ros.children():
          if rob.source_id().subdetector_id() == EventApps.TDAQ_CTP:
            ctp_rob = rob
            ctp_ros = ros

    if ctp_rob is None:
      sys.stdout.write('x')
      sys.stdout.flush()
      continue

    #else, we copy the CTP ROB data, faking the LVL2 result identifier
    new_event = EventApps.write.FullEventFragment(e)
    new_sd = EventApps.write.SubDetectorFragment()
    new_sd.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_LVL2, 0))
    new_event.append(new_sd)
    new_ros = EventApps.write.ROSFragment()
    new_ros.copy_header(ctp_ros)
    new_ros.source_id(EventApps.SourceIdentifier(EventApps.TDAQ_LVL2, 0))
    new_sd.append(new_ros)
    sys.stdout.write('.')
    sys.stdout.flush()
    out.write(new_event)
   
sys.stdout.write('\n')
sys.stdout.flush()
import os
rename_from = out.last_filename()
total = out.events_in_file()
del out # to close the output file
result = os.path.basename(sys.argv[1]) + '.withL2R'
os.rename(rename_from, result)
print "Saved file %s with %d events in it." % (result, total)
