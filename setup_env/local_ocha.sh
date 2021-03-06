#--------------------------------------------------------------------------
# tk/local_ocha.sh
#--------------------------------------------------------------------------
export TK_ROOT=$HOME/work/tk
export TK_CRON_CONF=$HOME/work/cron.conf
export PATH=${TK_SWDIR}/bin:$PATH
export LD_LIBRARY_PATH=${TK_SWDIR}/bin:$LD_LIBRARY_PATH

export workdir=/nfs/space3/tkohno/work
alias cds='cd /nfs/space3/tkohno'
export TK_SWDIR=/nfs/space3/tkohno/sw

export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

DIRSTACKSIZE=20
setopt autopushd

alias ise=/nfs/space1/local/Xilinx/14.5/ISE_DS/ISE/bin/lin64/ise

# export OCHA_SVN=svn+ssh://hpxr1.phys.ocha.ac.jp:/var/lib/svn
export OCHA_SVN=svn+ssh://hpx.phys.ocha.ac.jp/var/svn/repos
if [[ $LPDEST == "" ]]; then
    export LPDEST=hpxprint2
    export PRINTER=${LPDEST}
fi

# TexLive 2019
export MANPATH=/usr/local/texlive/2019/texmf-dist/doc/man:$MANPATH
export INFOPATH=/usr/local/texlive/2019/texmf-dist/doc/info:$INFOPATH
export PATH=/usr/local/texlive/2019/bin/x86_64-linux:$PATH

# Node/npm
alias setup_node='export PATH=/opt/node-v10.16.0-linux-x64/bin:$PATH'

# Scala
export PATH=/opt/scala-2.11.6/bin:$PATH
export CLASSPATH=/opt/scala-2.11.6/lib:$CLASSPATH

alias ssh_hpxr1="ssh -X -i ~/.ssh/id_rsa_hpxr1 tkohno@hpxsrv1"
alias ssh_hpxsrv1="ssh -X -i ~/.ssh/id_rsa_hpxr1 tkohno@hpxsrv1"
#----------------------------------------------------------------------
# ATLAS setup
#----------------------------------------------------------------------
# ATLAS setup using CVMFS
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
# ROOT
#export ROOTSYS=/nfs/opt/root-v5-34-07
function setup_root5() {
    export ROOTSYS=/nfs/opt/root-v5-34-32
    a=$(pwd); cd $ROOTSYS; source ./bin/thisroot.sh; cd $a
}
alias setup_root6='source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.16.00/x86_64-centos7-gcc48-opt/bin/thisroot.sh'
