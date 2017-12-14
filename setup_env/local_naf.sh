#--------------------------------------------------------------------------
# tk/local_naf.sh
#--------------------------------------------------------------------------

# Initial setup after login to NAF (atlas.naf.desy.de)

# Needed only once to enable the autoproxy mechanism
#ini glite
#ini autoproxy
#ap_gen.sh
#touch ~/.globus/.autoproxy

ini gliteatlas32
ini pandaclient
ini autoproxy
# once in a while need to do, ap_gen.sh
voms-proxy-info --all
alias naf_klog=/afs/naf.desy.de/group/atlas/software/help/naf_klog
ini dctools
ini ROOT53200

#kinit tkohno@CERN.CH
#kinit tkohno@DESY.DE

export TK_ROOT=$HOME/work/tk
export TK_CRON_CONF=$HOME/work/cron.conf

export sonasdir=/scratch/hh/dust/naf/atlas/user/tkohno
export lustredir=/scratch/hh/lustre/atlas/users/tkohno
export workdir=$sonasdir
export datadir=/scratch/hh/lustre/atlas/monthly/tkohno/data

export PATH=$lustredir/local/bin:$PATH
export LD_LIBRARY_PATH=${lustredir}/local/lib:$LD_LIBRARY_PATH
export PATH=$workdir/local/bin:$PATH
export LD_LIBRARY_PATH=${workdir}/local/lib:$LD_LIBRARY_PATH

export DCACHE_ATLAS=/pnfs/desy.de/atlas
export DCACHE_LOCALGROUPDISK=${DCACHE_ATLAS}/dq2/atlaslocalgroupdisk
export DCACHE_TKOHNO=${DCACHE_LOCALGROUPDISK}/user/tkohno/data
#dcap_header=dcap://dcache-ses-atlas.desy.de:22125
dcap_header=dcap://dcache-atlas-dcap.desy.de:22125

alias findother='qrsh -now n -l h_rt=10:00:00'

alias open_ssh_tunnel_pcatr17='ssh -L 10022:pcatr17.cern.ch:22 lxplus.cern.ch'
alias ssh_pcatr17='ssh -p 10022 localhost'

# dropboxd=${workdir}/local/Dropbox/.dropbox-dist/dropboxd
# if [[ -e ~/Dropbox && -e $dropboxd ]]; then
#     nl=$(ps -u tkohno | grep dropbox |wc -l)
#     if [[ $nl == 0 ]]; then;
# 	echo "Starting Dropbox daemon ..."
# 	$dropboxd &
#     fi
# fi

#--------------------------------------------------------------------------
# ATLAS setup
#--------------------------------------------------------------------------
ini atlas
# atlas_setup.py --create # creates cmthome and testarea

export AtlasSetup=/afs/naf.desy.de/group/atlas/software/releases/16.0.3/AtlasSetup
alias asetup="source $AtlasSetup/scripts/asetup.sh"

function asetupNightly() {
    export AtlasSetup=/afs/cern.ch/atlas/software/dist/AtlasSetup
    alias asetup="source $AtlasSetup/scripts/asetup.sh"
}
alias athena17.0.5.6='cd ~/athena/17.0.5.6; asetup AtlasProduction,17.0.5.6,here'
alias athena17.2.7.6='cd ~/athena/17.2.7.6; asetup AtlasProduction,17.2.7.6,cvmfs,here'
alias setup_dq2='ini -d gliteatlas32; ini dq2'

alias gridproxy='voms-proxy-init -voms atlas:/atlas/jp -valid 72:00:00'
