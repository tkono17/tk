#!/usr/bin/env zsh
#-------------------------------------------------------------------------
# Change file name
#-------------------------------------------------------------------------

function usage() {
    echo "Usage: $0 <match> <replace>"
    echo "Example: $0 \".hxx$\" \".h\""
}

match=''
replace=''

if [[ $# -lt 2 ]]; then
    usage $0;
    exit 1;
else;
    match=$1;
    replace=$2;
fi

echo "match  :$match"
echo "replace:$replace"

files=(`ls -1`)
for f0 in $files; do
    # echo "Checking file: $f0"
    f1=`echo $f0 | sed "s/$match/$replace/"`
    if [[ $f0 != $f1 ]]; then
	mv $f0 $f1;
	echo "Filename $f0 changed to $f1"
    fi
done
