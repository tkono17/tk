#!/usr/bin/env zsh

header=''
(( nlines=10 ))
filename=''
filebase='mu10.AOD'


function usage() {
    echo "$1: filename -n <nlines> -p <filebase> -h <header>"
}

# Read arguments
if [[ $# -ge 1 ]]; then
    filename=$1;
fi

if [[ ! -e $filename ]]; then
    usage $0
    exit 1
fi

a=(`cat $filename`)
(( iline=0 ))
(( ifile=0 ))
for line in $a; do
    if [[ $iline -eq 0 ]]; then
	out="$filebase.$ifile"
	if [[ -e $out ]]; then
	    rm $out;
	fi
    fi
    echo $line >> $out;
    (( iline = $iline + 1 ))
    if [[ $iline -eq $nlines ]]; then
	(( iline = 0 ))
	(( ifile = $ifile + 1 ))
    fi
done
