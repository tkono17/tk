#!/usr/bin/env zsh

fname_aod='/scratch/hh/lustre/atlas/monthly/tkohno/data/test/AOD.322405._000045.pool.root.1'

if [[ -e start_ara.py ]]; then
    rm start_ara.py
fi
echo "import user
import ROOT
import PyCintex
import AthenaROOTAccess.transientTree
print 'Import done. Opening file \"%s\"' % '${fname_aod}'
f = ROOT.TFile.Open('${fname_aod}')
tt = AthenaROOTAccess.transientTree.makeTree(f)
print 'Transient tree tt available'
" > start_ara.py

echo "Run the following line in python to setup ARA\n"
echo "execfile('start_ara.py')\n"
python

