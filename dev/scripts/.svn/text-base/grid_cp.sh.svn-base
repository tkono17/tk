#!/usr/bin/env zsh

grid_type='lcg'
grid_dir=''
grid_file=''
file_list=''


function usage() {
    echo "Usage: $1 <options>"
    echo "------"
    echo "Options: -t <type> ....... Type of the grid"
    echo "         -d <griddir> .... Directory name on the grid"
    echo "         -f <filename> ... File name to be copied from the grid"
    echo "         -l <filelist> ... File containing the list of files to be retrieved"
    echo "Examples:"
    echo "  > $1 -t lcg -d \"lfn:/grid/...\" -l AODlist.txt"
}

function lcg_cp() {
    # $1=grid_file
    grid_abspath=${grid_dir}/$1;
    lcg-cp --vo atlas ${grid_abspath} file:`pwd`/$1;
}

if [[ $# -eq 0 ]]; then
    usage $0;
    exit 1;
fi

while getopts t:d:f:l: opt; do
    myarg=""
    myarg=$OPTARG
    case $opt in
	"t")
	    grid_type=$OPTARG;;
	"d")
	    grid_dir=$OPTARG;;
	"f")
	    grid_file=$OPTARG;;
	"l")
	    file_list=$OPTARG;;
	":"|"?")
	    echo "Wrong argument";;
    esac
    echo "o=$opt, myarg=$OPTARG";
done

exit 0;


files=(`cat aod.txt`)
for f in $files; do
    case $grid_type in 
	"lcg")
	    lcg_cp $f;;
	*)
	    echo "Unknown GRID type : $grid_type"
	    break;;
    esac
done

