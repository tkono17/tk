#!/usr/bin/env zsh

function usage() {
    # echo "Usage: $1 <L1config.xml>"
echo "Usage: $1 <triggerPythonConfig_file.py>"
}

if [[ $# -ne 1 ]]; then
    usage $0
    exit 1
fi

fname=$1;

pat_item="s/[ [:alnum:]_=]\+LVL1MenuItem('\(L1[[:alnum:]_]\+\)'[[:alnum:] _=.(),'\\]\+/'\1': 1/"
pat_item_ps="s/[ [:alnum:]_=]\+LVL1MenuItem('\(L1[[:alnum:]_]\+\)'[[:alnum:] _=.(),'\\]\+/'\1': \2,/"

rm -fr all_items.txt items_with_ps.txt

grep item_ $fname |grep "L1_" | sed "$pattern" |grep -v '^[ ]*#' > all_items.txt


