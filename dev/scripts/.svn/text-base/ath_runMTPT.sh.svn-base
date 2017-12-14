#!/usr/bin/env zsh

jo1=TriggerRelease/Trigger_topOptions_writeBS.py
jo2=TriggerRelease/runHLT_standalone.py

rdo=/rscratch/pcatr18/tkohno/data/RDO.211882._000028.pool.root.1
bs=bs.data

if [[ -e b1.log ]]; then
    rm b1.log
fi
#athena.py -c "PoolRDOInput=['$rdo'];BSRDOOutput='$bs';setMenu='Physics_pp_v2';setDetDescr='ATLAS-GEO-16-00-00'" $jo1 >& b1.log

opt='testMCV3=True'

if [[ -e b2.log ]]; then
    rm b2.log
fi
athenaMT.py -n 20 -f $bs -o mt -c $opt $jo2 >& b2.log

if [[ -e b3.log ]]; then
    rm b3.log
fi
athenaPT.py -n 20 -f mt-1.__0001.data -c $opt $jo2 >& b2.log

 

