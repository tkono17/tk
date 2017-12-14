#!/usr/bin/env zsh

dir=$DCACHE_TKOHNO
if [[ $# -gt 1 ]]; then
    dir=$1
fi
aaa=(`dcls $dir`)

for a in $aaa; do
    if [[ -e tmp.txt ]]; then rm -fr tmp.txt; fi
    dq2-list-files $a > tmp.txt
    n=$(grep 'total files: ' tmp.txt | sed "s/total files: //")
    s=$(grep 'total size: ' tmp.txt | sed "s/total size: //")
    #dcls -l $dir/$a
    echo "$a => $n files, $s B"
done
