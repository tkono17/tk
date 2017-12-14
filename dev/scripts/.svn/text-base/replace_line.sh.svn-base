#!/usr/bin/env zsh

fname=$1;
pat=$2;
out=$3;

# echo "Replace the pattern '$pat' with '$out' in file $fname"

bname=`basename $fname`
tmp=/tmp/${bname}_XYZabc.tmp.txt
tmpdiff=/tmp/${bname}_XYZabc.tmpdiff.txt
rm -f $tmp;
rm -f $tmpdiff;

sed "s/$pat/$out/g" $fname > ${tmp}
diff $fname $tmp > $tmpdiff
if [[ -s ${tmpdiff} ]]; then
    # echo "Replacing file with the update"
    mv ${tmp} $fname
else;
    echo "No pattern found in file $fname"
fi



