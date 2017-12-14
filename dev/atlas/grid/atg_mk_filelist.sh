#!/usr/bin/env zsh
#--------------------------------------------------------------------
# Create list of files in a given dataset for each site with replica
#--------------------------------------------------------------------

dataset=""

function usage() {
    echo "This script creates a list of files available on LCG grid sites"
    echo "for a given ATLAS dataset. It uses the DQ2 client tool to get the"
    echo "necessary information"
    echo "Usage: $1 <dataset>"
}


while getopts h opt; do
    case $opt in
	"h")
	    usage $0
	    exit 0;;
    esac
done


dq2_ls -h >& /dev/null
if [[ $? != 0 ]]; then
    echo "Problem with DQ2 end clients tool (dq2_ls -h finished with error)"
    echo "  Maybe DQ2 environment is not setup properly"
    exit 1
fi

if [[ $# -ne 1 ]]; then
    usage $0
    exit 2
else
    dataset=$1
fi

#--------------------------------------------------------------------
# Main script
#-------------
files_and_sites="files_and_sites.txt"
all_files="all_files.txt"
all_sites="all_sites.txt"
rm -f $files_and_sites $all_files $all_sites
rm -f $all_files $all_sites

dq2_ls -g -r "$dataset" > $files_and_sites
grep " $dataset" $files_and_sites | grep -v Replica | \
    grep -v "^[a-zA-Z0-9]" | sed "s/ //g" > $all_files
grep "Replica" $files_and_sites | \
    sed "s/[ ]\+\([a-zA-Z0-9.-]\+\)[ ]\+[- a-zA-Z0-9]\+/\1/" | \
    sed "s/ //g" > $all_sites

sites=(`cat $all_sites`)
for site in $sites; do
    fout="lfn_in_$site.txt"
    rm -f $fout
    dq2_ls -f -s $site $dataset > $fout
    fout="pfn_in_$site.txt"
    rm -f $fout
    dq2_ls -f -p -s $site $dataset > $fout
done

sites=(LYON CERN MILANO NIKHEF TRIUMF RAL SARA PIC FZK
    CNAF NDGFT1 NAPOLI ASGC BNL)
assigned_lfns="assigned_lfns.txt"
rm -f $assigned_lfns
touch $assigned_lfns
((total=0))
for site in $sites; do
    f=lfn_in_$site.txt
    if [[ ! -e $f ]]; then
	continue
    fi
    rm -f temp temp2 temp3
    grep '^ ' $f | sed "s/ //g" > temp
    a=(`wc -l temp`)
    filter_lines.py -m temp $all_files > temp3
    filter_lines.py temp3 $assigned_lfns > lfns_to_run_at_$site.txt
    b=(`wc -l temp2`)
    cat lfns_to_run_at_$site.txt >> $assigned_lfns
    if [[ -z $assigned_lfns ]]; then
	rm $assigned_lfns
    fi
    echo "$b[1]/$a[1] at site $site"
    (( total = $total + $b[1] ))
done
echo "Total number of files to run from all sites: $total"
echo "Missing files:"
filter_lines.py $all_files $assigned_lfns


