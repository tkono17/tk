#!/usr/bin/env python
#-------------------------------------------------------------------------
# Create a LVL1 result fragment sent from the LVL1 system to LVL2
# using the LVL1 DAQ data.
#-------------------------------------------------------------------------
import sys
import EventApps

def usage():
  print 'usage: %s <input-file> [<nevents>=-1] ' % sys.argv[0]
  sys.exit(1)

nevents = -1
input_file = ''

if len(sys.argv) not in [ 2, 3 ]:
  usage()


if len(sys.argv)>1: input_file = sys.argv[1]
if len(sys.argv)>2: nevents = int(sys.argv[2])

print 'input_file = ', input_file
print 'nevents = ', nevents

input = EventApps.istream(input_file)

ievent = 0
robs = []

for event in input:
  for subdet in event.children():
    for ros in subdet.children():
      for rob in ros.children():
        robid = rob.source_id().code()
        if robid not in robs:
          robs.append(robid)
  ievent += 1
  if ievent == nevents: break

for r in robs:
  print "%08x" % r
  
sys.exit(0)
