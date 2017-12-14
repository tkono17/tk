#!/usr/bin/env zsh

zparseopts -a $* r:=runs t:=triggers d::=dest

echo "runs = $runs"
echo "triggers = $triggers"
echo "destination = $dest"

if [[ ${#runs} == 2 && ${#triggers} == 2 ]]; then
    cd /tmp/tkohno
    echo "TestArea=$TestArea"
    if [[ $TestArea == "" ]]; then
	echo "Setting up athena environment"
	source $AtlasSetup/scripts/asetup.sh AtlasProduction,16.6.7.3,here
	echo "TestArea set to $TestArea"
    fi
    runs=($(echo ${runs[2]} | sed "s/,/ /g" ))
    triggers=${triggers[2,-1]}
    for r in $runs; do
	echo "Make Lumi/PS ntuple for run=$r"
	root -l -b -q '$TK_ROOT/root/atlas/mk_lumips_ntuple.C+('$r', "'$triggers'")'
    done

    if [[ $dest != "" ]]; then
	scp lumips*.root $dest;
    fi
fi

