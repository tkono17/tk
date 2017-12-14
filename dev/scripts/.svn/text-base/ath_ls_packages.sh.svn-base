#!/usr/bin/env zsh

function usage() {
    echo "Usage: $1 [<dir>=$TestArea]"
}

if [[ $# -gt 1 ]]; then
    usage $0;
    exit 1
fi

while getopts h opt; do
    case $opt in
	"h")
	    usage $0;
	    exit 0;
    esac
done


p=$TestArea
if [[ $# -gt 0 ]]; then
    p=$1;
fi

if [[ $p == "" ]]; then
    usage $0;
    exit 2;
fi

((n=${#p} + 2))
find $p -name requirements | grep -v cmthome | cut -c $n- |\
    sed "s/\/cmt\/requirements//g"
