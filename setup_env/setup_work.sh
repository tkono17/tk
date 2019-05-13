#--------------------------------------------------------------------------
# tk/setup_work.sh
#--------------------------------------------------------------------------

##### My setup
export TKDEV_ROOT=$TK_ROOT/dev
export PATH=$TK_ROOT/bin:$PATH
export LD_LIBRARY_PATH=$TK_ROOT/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$TK_ROOT/python:$PYTHONPATH
export PATH=$TK_SWDIR/bin:$PATH
export LD_LIBRARY_PATH=$TK_SWDIR/lib:$LD_LIBRARY_PATH

##### ATLAS settings
alias uuidgen='uuidgen | tr "[:lower:]" "[:upper:]"'
#if [[ ! -d $AtlasSetup ]]; then
#    export AtlasSetup=/afs/cern.ch/atlas/software/dist/AtlasSetup
#fi
#if [[ -d $AtlasSetup ]]; then
#    alias asetup="source $AtlasSetup/scripts/asetup.sh"
#fi
export RUCIO_ACCOUNT=tkohno
export AMIConfFile=$HOME/private/ami.conf
# Trigger stuffs
export TRIGGER_EXP_CORAL_PATH=/afs/cern.ch/user/a/attrgcnf/.expertauth
alias rateHistory=/afs/cern.ch/user/a/aagaard/public/rateHistory/rateHistory.sh
function draw_rates() {
    cmd=/afs/cern.ch/user/h/hristova/public/draw_rates.py
    source /afs/cern.ch/atlas/project/tdaq/cmt/bin/cmtsetup.sh tdaq-04-00-01
    export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
    export PATH=/afs/cern.ch/atlas/project/tdaq/inst/sw/lcg/external/Python/2.6.5/i686-slc5-gcc43-opt/bin:$PATH
    $cmd
}

alias naf=". /afs/cern.ch/project/gd/LCG-share/current/etc/profile.d/grid-env.sh; voms-proxy-init -voms atlas -rfc; gsissh -Y atlas.naf.desy.de"
alias makeq='make QUICK=1'

alias bastion='ssh -Y tkohno@bastion.desy.de'
alias atlas-wgs='ssh -Y tkohno@atlas-wgs.desy.de'
alias lxplus='ssh -Y tkohno@lxplus.cern.ch'
alias icepp='ssh -Y tkohno@login.icepp.jp'
alias pcatr17='ssh -Y tkohno@pcatr17.cern.ch'
alias pcatr23='ssh -Y tkohno@pcatr23.cern.ch'
alias setup_slc5="source ${TK_ROOT}/dev/scripts/setup_slc5.sh"

export SVNROOT=svn+ssh://svn.cern.ch/reps/atlasoff
export SVNUSR=svn+ssh://svn.cern.ch/reps/atlas-tkohno
export SVNGRP=svn+ssh://svn.cern.ch/reps/atlasgroups

export _JAVA_OPTIONS="-Xms256m -Xmx1024m"

# alias gridproxy='voms-proxy-init -voms atlas:/atlas/jp -valid 72:00:00'
alias gridproxy='voms-proxy-init -voms atlas -valid 72:00:00'
export ALRB_rootVersion="6.14.04-x86_64-slc6-gcc62-opt"
