#--------------------------------------------------------------------------
# tk/local_laptop.sh
#--------------------------------------------------------------------------
export TK_ROOT=$HOME/work/tk
export TK_CRON_CONF=$HOME/work/cron.conf

#export ROOTSYS=/opt/root_v6.14.00
#cd $ROOTSYS; source ./bin/thisroot.sh; cd - >& /dev/null;
source /opt/root_v6.20.04/bin/thisroot.sh
#export PATH=$ROOTSYS/bin:$PATH
#export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH

#export tk_svnroot=svn+ssh://tkohno@lxplus.cern.ch/afs/cern.ch/user/t/tkohno/scratch0/svnroot/repos

#alias ise=/opt/products/Xilinx/14.6/ISE_DS/ISE/bin/lin/ise

export PATH=/opt/node-v10.16.0-linux-x64/bin:$PATH
