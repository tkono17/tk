#!/usr/bin/env zsh
#---------------------------------------------------------------------
# Make analysis directory with ROOT environment
# --------
# Contains
# data/  doc/  figures/  files/  macros/  rootlogon.C  work/
#---------------------------------------------------------------------

function usage() {
    echo "Usage: $0 [options] <project_name>"
    echo "------"
    echo "Options: -h ..... help"
    echo "Examples: $0 ."
    echo "          $0 my_project"
}

#------------------------------------
# parse arguments
#------------------------------------
while getopts 'hab' opt $*; do
    echo "opt=$opt IND=$OPTIND"
    case $opt in
	a|b)
	    continue;;
	h)
	    usage
	    exit 1;;
	*)
	    echo "Unknown option: $opt"
	    usage
	    exit 1;;
    esac
done

(( narg = $# - $OPTIND + 1 ))
if [[ $narg -ne 1 ]]; then
    usage
    exit 1
fi

project_name=${*[$OPTIND]}
dirs=(data doc figures files macros work)
macros=(my*.[hC] chk_tree.C *_utils.[hc]xx Plotter.[hc]xx)

cwd=`pwd`
if [[ $project_name != "." ]]; then
    mkdir -p $project_name;
    cd $project_name;
fi

for d in $dirs; do
    mkdir -p $d;
done

macro_files=(`(cd $TK_ROOT/root; ls $macros)` )
if [[ ${#macro_files} -ge 1 ]]; then
    for f in ${macro_files}; do
	ln -s ${TK_ROOT}/root/$f macros/$f
    done
fi
cp $TK_ROOT/root/rootlogon.C .
cp $TK_ROOT/root/dot-rootrc .rootrc

cd $cwd;



