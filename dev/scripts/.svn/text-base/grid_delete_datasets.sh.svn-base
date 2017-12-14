#!/usr/bin/env zsh

def usage() {
    echo "Usage: $0 <dataset_list> (can be the output of list_dcache.txt)"
    echo "------"
    echo "   The dataset list should contain a list of datasets to be deleted"
    echo "   For each line, the first word is recognized as the dataset name"
    echo "   For example, it can be the output of list_dcache.txt"
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

flist=$1;
datasets=( $(cat $flist | awk '{ printf("%s\n", $1); }') )
echo "${#datasets} datasets to be deleted"
for d in $datasets; do
    dq2-delete-replicas -a $d
done

