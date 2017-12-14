#!/usr/bin/env zsh

packages=(
    Trigger/TrigHypothesis/TrigEgammaHypo
    Trigger/TriggerCommon/TriggerMenuPython
    Trigger/TriggerCommon/TriggerMenuXML
    Trigger/TrigAnalysis/TriggerMenuNtuple
    Trigger/TrigAnalysis/TriggerMenuAnalysis
    PhysicsAnalysis/D3PDMaker/TrigEgammaD3PDMaker
    # Trigger/TrigAnalysis/TrigDecisionTool
    # Trigger/TrigT1/TrigT1TGC
)

nightlies=(
    devval/AtlasTrigger
    devval/AtlasAnalysis
    dev/AtlasTrigger

    16.6.X.Y/AtlasProduction
    16.6.X.Y-VAL/AtlasProduction

    16.1.X.Y-VAL/AtlasP1HLT
    16.1.X.Y-VAL2/AtlasP1HLT
    16.1.X.Y.Z-VAL/AtlasCAFHLT
    16.1.X.Y.Z-VAL2/AtlasCAFHLT
)

nightly_dir=/afs/cern.ch/atlas/software/builds/nightlies
nightly_rel=rel_0

function usage() {
    echo "Usage: $1 [options]"
    echo "------"
    echo "Options: -h ........... Help"
    echo "         -r <rel> ..... Release (rel_0 etc.)"
}

while getopts hr: opt $*; do
    case $opt in 
	"h") usage $0;
	    exit 0;;
	"r") nightly_rel=$OPTARG;;
    esac
done

for n in $nightlies; do
    echo "#----- Nightly ${n} ${nightly_rel}"
    for p in $packages; do
	version_file=${nightly_dir}/${n}/${nightly_rel}/${p}/cmt/version.cmt
	if [[ -e $version_file ]]; then
	    echo "  "`cat $version_file`
	fi
    done
done

