#--------------------------------------------------------------------------
# tk/local_icepp.sh
#--------------------------------------------------------------------------
export TK_ROOT=${HOME}/work/tk
export TK_SWDIR=$HOME/sw
export TK_CRON_CONF=$HOME/work/cron.conf

export workdir=/gpfs/fs2001/tkohno
export datadir=/gpfs/fs2001/tkohno/data

export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

DIRSTACKSIZE=20
setopt autopushd

# Setup gcc,python,root,boost
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5/setup.sh
#Python
#dir0=/afs/cern.ch/sw/lcg/external/Python/2.7.3/x86_64-slc5-gcc47-opt
#export PATH=${dir0}/bin:${PATH}
#export LD_LIBRARY_PATH=${dir0}/lib:${LD_LIBRARY_PATH}
#ROOT
#export ROOTSYS=/afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.09/x86_64-slc5-gcc47-opt/root
#dir0=$(pwd)
#cd ${ROOTSYS}; source ./bin/thisroot.sh; cd ${dir0}
#BOOST
#export BoostDir=/afs/cern.ch/sw/lcg/external/Boost/1.53.0_python2.7/x86_64-slc5-gcc47-opt
alias cds='cd $workdir'

#--------------------------------------------------------------------------
# ATLAS setup
#--------------------------------------------------------------------------
#export PATHENA_GRID_SETUP_SH=/afs/icepp.jp/project/gd/LCG-share/current/etc/profile.d/grid_env.sh
#source $PATHENA_GRID_SETUP_SH

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
alias setup_grid='source /afs/icepp.jp/project/gd/LCG-share/current/etc/profile.d/grid-env.sh'

#setupATLAS >& /dev/null

#which root |grep '/cvmfs' >& /dev/null
#if [[ $? != 0 ]]; then
#    localSetupROOT
#fi
alias setupFrontier='export FRONTIER_SERVER=$FRONTIER_SERVER"(proxyurl=http://conddb-px02.icepp.jp:3128)"'

#export AtlasSetup=/afs/icepp.jp/atlasjp/software/releases/17.2.7/AtlasSetup

#alias athena17.2.7.9='cd ${HOME}/athena/17.2.7.9; asetup AtlasProduction,17.2.7.9,here'
#alias athena17.2.10.1='cd ${HOME}/athena/17.2.10.1; asetup AtlasProduction,17.2.10.1,here'
alias athena20.0.0.1='cd ${workdir}/athena/20.0.0.1; asetup AtlasProduction,20.0.0.1,64,gcc48,here'

#alias setup_grid='source /afs/icepp.jp/project/gd/LCG-share/current/external/etc/profile.d/grid-env.sh'

#alias setup_panda='source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh'
#alias setup_dq2='source /afs/icepp.jp/atlasjp/offline/external/DQ2Clients/setup.sh'


