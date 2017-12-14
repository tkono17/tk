#!/usr/bin/env zsh

rdo="/scratch/hh/lustre/atlas/monthly/tkohno/data/test/RDO.211882._000027.pool.root.1"
bs="bs.data"

jo=TriggerRelease/Trigger_topOptions_writeBS.py

if [[ -e a.log ]]; then
    rm a.log
fi
if [[ -e $bs ]]; then
    rm $bs
fi

c="PoolRDOInput=['$rdo'];"
c="$c;setMenu='Physics_pp_v2';"
c="$c;BSRDOOutput='$bs'"

athena.py -c $c $jo >& a.log
