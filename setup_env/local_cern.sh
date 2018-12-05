#--------------------------------------------------------------------------
# tk/local_cern.sh
#--------------------------------------------------------------------------

alias kinit=/usr/sue/bin/kinit

if [[ $HOST == atdesy9 ]]; then
    xset m 5 10
fi

export TK_CRON_CONF=$HOME/work/cron.conf

# a=$(cat /etc/motd | grep 'Scientific Linux CERN 6' | wc -l)
a=$(cat /etc/motd | grep 'SLC' | grep '6\.' | wc -l)
if [[ $a == 1 ]]; then
    . /afs/cern.ch/sw/lcg/contrib/gcc/4.7/x86_64-slc6/setup.sh
    set adir=$(pwd)
    cd /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.19/x86_64-slc6-gcc47-opt/root;
    . ./bin/thisroot.sh
    cd ${adir}
    unset adir
fi
a=

export TK_ROOT=$HOME/work/tk
export TK_CRON_CONF=$HOME/work/cron.conf

export workdir=/afs/cern.ch/work/t/tkohno
export datadir=/afs/cern.ch/work/t/tkohno/data
export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

export TK_SWDIR=$workdir/sw

export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$workdir/local/lib/python2.6/site-packages:$PYTHONPATH


##### ATLAS settings
export AtlasSetup=/afs/cern.ch/atlas/software/dist/AtlasSetup
alias triggerTool=/afs/cern.ch/user/a/attrgcnf/TriggerTool/run_TriggerTool_interactive.sh

##### CASTOR setting
export RFIO_USE_CASTOR_V2=YES
export STAGE_HOST=castoratlas
export STAGE_SVCCLASS=default

#export PRINTER=40-5D-471
# export PRINTER=104-RC12-HP3015
export PRINTER=32-SB02-CANON
export LPDEST=${PRINTER}

