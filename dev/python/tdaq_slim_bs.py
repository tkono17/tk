#!/usr/bin/env python
#-------------------------------------------------------------------------
# Slim bytestream file
#-------------------------------------------------------------------------
import sys
import EventApps

def usage():
  print 'usage: %s <input-file> <nevents> <First_Lvl1Id>=-1' % sys.argv[0]
  sys.exit(1)

nevents = -1
input_file = ''
l1id0 = -1

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
    #    for subdet in event.children():
    #        for ros in subdet.children():
    #            for rob in ros.children():
    ievent += 1
    output.write(event)
    if ievent == nevents: break

print 'Wrote %d events in %s' % (output.events_in_file(),
                                 output.current_filename())

sys.exit(0)
