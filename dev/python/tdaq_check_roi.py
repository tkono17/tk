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

  print '***** Event'
  for sd in e.children():
    if sd.source_id().subdetector_id() == EventApps.TDAQ_LVL2:
      for ros in sd.children():
        for rob in ros.children():
          subdet_id = rob.source_id().subdetector_id()
          module_id = rob.source_id().module_id()
          if subdet_id == EventApps.TDAQ_CTP and \
                 module_id == 0x1:
            data = rob.rod_data()
            print 'Number of CTP words: %d' % len(data)
            for i in range(8):
              print 'CTP word %d: %08x' % (i, data[24+i])
          elif subdet_id == EventApps.TDAQ_MUON_CTP_INTERFACE and \
                   module_id == 0x1:
            print 'Number of muon RoI: %d' % len(rob.rod_data())
            for i in range(0, len(rob.rod_data())):
              print 'RoI: %08x' % rob.rod_data()[i]
            

##     sys.stdout.write('.')
##     sys.stdout.flush()
##     out.write(new_event)
   
## sys.stdout.write('\n')
## sys.stdout.flush()
## import os
## rename_from = out.last_filename()
## total = out.events_in_file()
## del out # to close the output file
## result = os.path.basename(sys.argv[1]) + '.withMuRoI'
## os.rename(rename_from, result)
## print "Saved file %s with %d events in it." % (result, total)
