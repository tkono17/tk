#--------------------------------------------------------------------------
# tk/local_desy.sh
#--------------------------------------------------------------------------
export TK_ROOT=$HOME/work/tk
export TK_SWDIR=$HOME/sw
export TK_CRON_CONF=$HOME/work/cron.conf

export workdir=/atlas/discs/pool03/tkohno/
export datadir=/atlas/discs/pool03/tkohno/data

export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

ini root532
#export ROOTSYS=/afs/naf.desy.de/products/root/amd64_rhel50/5.30.00
#(cd $ROOTSYS; source ./bin/thisroot.sh)

alias firefox=/afs/desy.de/group/atlas/software/firefox/firefox-10.0.2/firefox
alias gridproxy='voms-proxy-init -voms atlas:/atlas/jp -valid 72:00:00'
