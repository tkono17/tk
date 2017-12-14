#!/usr/bin/env zsh
#-----------------------------------------------------------------------
# Check missing datasets using dq2 tools
#-----------------------------------------------------------------------

dataset_name=
is_container=no
site=DESY-HH_LOCALGROUPDISK

function usage() {
    echo "Usage: $0 <dataset> [<site>=DESY-HH_LOCALGROUPDISK]"
}

if [[ $# -eq 0 ]]; then
    usage
    exit 1;
fi

which dq2-ls >& /dev/null
if [[ $? != 0 ]]; then
    echo "DQ2 tools not available."
    exit -1;
fi

dataset_name=$1;
if [[ $# -ge 2 ]]; then
    site=$2;
fi

datasets=()
if [[ ${dataset_name[-1]} == '/' ]]; then
    is_container=yes
    datasets=($(dq2-list-datasets-container $dataset_name))
else
    datasets=($dataset_name)
fi

echo "Input dataset: $dataset_name"
echo "${#datasets} datasets to check"
for ds in $datasets; do
    good=$(dq2-list-dataset-replicas $ds | grep ' COMPLETE: ' |grep $site)
    if [[ $good != "" ]]; then
	echo "  $ds -> Available at $site"
    else
	echo "  $ds -> NOT available at $site"
    fi
done

