#!/usr/bin/env zsh

fname=
if [[ $# == 1 ]]; then
    fname=$1
else
    echo "Usage: $0 <d3pd_maker_cxx>"
    exit -1
fi

a=(`grep CHECK $fname | \
    sed "s/.*addVariable.*(//g" | sed "s/,.*//g" | sed 's/"//' | \
    sed 's/"/ /'`)
echo "\n$a\n"

