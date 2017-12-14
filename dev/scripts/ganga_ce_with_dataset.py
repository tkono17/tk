#--------------------------------------------------------------------------
# Search ComputingElements on the grid which has a certain dataset
#-----
# This is a python file to be given to ganga
#--------------------------------------------------------------------------
import sys

def usage():
    print 'Usage: %s <dataset>' % (sys.argv[0])

# Parameters
dataset_name=''

if len(sys.argv)!=2:
    usage()
    sys.exit(0)


sys.exit(-1)

dataset_name = sys.argv[1]


ds = DQ2Dataset()
ds.list_locations_ce(dataset_name)
