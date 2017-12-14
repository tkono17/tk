#!/usr/bin/env zsh
#--------------------------------------------------------------------------
# Search ComputingElements on the grid which has a certain dataset
#-----
# This is a python file to be given to ganga
#--------------------------------------------------------------------------

function usage() {
    echo "Usage: ganga_ce_with_dataset.sh <dataset_name> "
}

dataset=''

if [[ $# -eq 1 ]]; then
    dataset=$1;
else
    usage
    exit -1
fi

tmpfile=ganga_tmp

rm -f $tmpfile
echo "ds = DQ2Dataset()" > $tmpfile
echo "ds.list_locations_ce('$dataset')" >> $tmpfile
echo "ds.list_locations_num_files('$dataset')" >> $tmpfile
echo "print 'bye'" >> $tmpfile

echo "# Searching CE with dataset '$dataset'"
ganga $tmpfile >& ce_search.out

# Imcomplete datasets
echo "Imcomplete datasets:"
imcomplete_ce=(`grep '^Incomplete:' ce_search.out | sed -e 's/^Incomplete://'`)
for ce in $imcomplete_ce; do
    echo "ce: $ce"
    ganga_ce_info.sh $ce
done

grep "{'" ce_search.out

# Complete datasets
