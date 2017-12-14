#!/usr/bin/env zsh

#------------------------------------------------------------------------
# Configuration data (list of datasets)
#------------------------------------------------------------------------
typeset -A datasetMap
function setDatasetsFromDict() {
    fname=$1
    python <<EOF
execfile("$fname")
values = datasets.values()
values.sort()
fout = open('dataset_names.txt', 'w')
for d in values:
  fout.write('%s\n' % d)
fout.close()
EOF
    datasets=($(cat dataset_names.txt))
}

#------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------
function setup() {
    mkdir -p /tmp/tkohno/ami
    cd /tmp/tkohno/ami
    #cmd=/afs/cern.ch/atlas/software/builds/AtlasCore/17.0.1/Database/Bookkeeping/AMIClients/pyAMI/share/makeAMICommandList.py
    cmd=makeAMICommandList.py
    $cmd
#    if [[ -e aliasMaker.sh ]]; then
#	rm aliasMaker.sh
#    fi
    #cat aliasMaker.sh | sed "s/17.0.1/16.6.6/g" > aliasMaker2.sh
    echo "Execute : source /tmp/tkohno/ami/aliasMaker.sh"
    #rm -fr aliasMaker*sh
}

function strip_slash() {
    x=$1
    if [[ ${#x} -gt 1 && ${x[-1]} == '/' ]]; then
	x=${x[1,-2]}
    fi
    echo $x
}

function find_provenance() {
    ds=$(strip_slash $1)
    type=$2
    r="???"
#     # AMI provenance is restricted now
#     out=($(amiListDatasetProvenance $ds | grep $type))
#     if [[ ${#out} -ge 1 ]]; then
# 	r=${out[1]}
#     fi
    if [[ $type == "EVNT" ]]; then
	a=($(echo $ds | sed "s/merge.AOD./evgen.EVNT.\n/"))
	if [[ ${#a} -eq 2 ]]; then
	    b=($(echo ${a[2]} | sed "s/_/\n/g"))
	    if [[ ${#b} -ge 1 ]]; then
		r="${a[1]}${b[1]}"
	    fi
	fi
    fi
    echo $r
}

function list_evntInfo() {
    ds=$(strip_slash $1)
    evnt=$ds
    x=($(echo $ds | grep EVNT))
    if [[ ${#x} -eq 1 ]]; then
	evnt=$ds
    else
	evnt=$(find_provenance $ds EVNT)
    fi
    pat='logicalDatasetName|totalEvents|GenFiltEff_mean|crossSection_mean'
    #which amiGetDatasetEVNTInfo
    amiGetDatasetEVNTInfo $evnt | egrep $pat
}

#------------------------------------------------------------------------
# Parse arguments
#------------------------------------------------------------------------
zparseopts s=setup l=list i:=input_file

#------------------------------------------------------------------------
# Main program
#------------------------------------------------------------------------
mkdir -p /tmp/tkohno
cd /tmp/tkohno

if [[ ${#setup} == 1 && ${setup[1]} == -s ]]; then
    setup
fi
if [[ ${#list} == 1 && ${list[1]} == -l ]]; then
    if [[ ${#input_file} != 2 ]]; then
	echo "-l option must be used with -i <filename.py>"
	exit 1;
    fi
    if [[ -e /tmp/tkohno/ami/aliasMaker2.sh ]]; then
	source /tmp/tkohno/ami/aliasMaker2.sh
    else
	echo "Run ath_ami.sh -s first to setup the environment"
    fi
    setDatasetsFromDict ${input_file[2]}
    for ds in ${datasets}; do
	echo "#------------------------------------------------------------------"
	echo "# $ds"
	list_evntInfo $ds
	echo ""
    done
fi

