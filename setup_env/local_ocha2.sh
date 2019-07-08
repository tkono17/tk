#--------------------------------------------------------------------------
# tk/local_ocha.sh
#--------------------------------------------------------------------------
export TK_ROOT=$HOME/work/tk
export TK_SWDIR=$HOME/sw
export TK_CRON_CONF=$HOME/work/cron.conf
export PATH=${TK_SWDIR}/bin:$PATH
export LD_LIBRARY_PATH=${TK_SWDIR}/bin:$LD_LIBRARY_PATH

# Needed for OpenFOAM6
export PATH=/usr/lib64/openmpi3/bin:$PATH
export LD_LIBRARY_PATH=/usr/lib64/openmpi3/lib:$LD_LIBRARY_PATH
# source $HOME/OpenFOAM/OpenFOAM-dev/etc/bashrc

export workdir=/nfs/space1/tkohno/work
alias cds='cd /nfs/space1/tkohno'

export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

DIRSTACKSIZE=20
setopt autopushd

export OCHA_SVN=svn+ssh://hpx.phys.ocha.ac.jp/var/svn/repos
export LPDEST=hpxprint2
export PRINTER=${LPDEST}

# Japanese input method
export GTK_IM_MODULE=ibus
export XMODIFIERS=@im=ibus
export QT_IM_MODULE=ibus
#ibus-daemon -d -x

# Scala
export PATH=/opt/scala-2.11.6/bin:$PATH
export CLASSPATH=/opt/scala-2.11.6/lib:$CLASSPATH

#----------------------------------------------------------------------
# ATLAS setup
#----------------------------------------------------------------------
# ATLAS setup using CVMFS
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
# ROOT
#export ROOTSYS=/nfs/opt/root-v5-34-07
#export ROOTSYS=/nfs/opt/root-v5-34-32
#a=$(pwd); cd $ROOTSYS; source ./bin/thisroot.sh; cd $a

# alias setup_vivado='source /opt/Xilinx/Vivado/2017.3/settings64.sh'
alias setup_vivado='source /home/opt/Xilinx/Vivado/2018.2/settings64.sh'
alias setup_sdk='source /home/opt/Xilinx/SDK/2018.2/settings64.sh'
alias setup_petalinux='source /home/tkono/work/Xilinx/petalinux/settings.sh'

export AdminDn=cn=Manager,ou=hpx,dc=phys,dc=ocha,dc=ac,dc=jp
export BaseDn=ou=hpx,dc=phys,dc=ocha,dc=ac,dc=jp
