#!/usr/bin/env zsh
#--------------------------------------------------------------------
# Run query
#--------------------------------------------------------------------

s_find=
s_show=
lock_find=no
lock_show=no

function addFindCond() {
    if [[ $lock_find != yes ]]; then
	if [[ $s_find == "" ]]; then
	    s_find=$1
	else
	s_find="$s_find and $1"
	fi
    fi
}

function addShowCond() {
    if [[ $lock_show != yes ]]; then
	if [[ $s_show == "" ]]; then
	    s_show=$1
	else
	    s_show="$s_show and $1"
	fi
    fi
}

function usage() {
    echo "Usage: $1 [options]"
    echo "------"
    echo "Options: -L <n_runs> ........... "
    echo "         -H <n_hours>h ......... "
    echo "         -R <run> .............. "
    echo "         --dq <DQ_query> ....... Data quality query"
    echo "         --gr2009 .............. Good runs for 2009 runs"
    echo "         --gr2010-04 ........... Good runs for 2010 runs as of Apr. 2010"
    echo "         --gr2010-05 ........... Good runs for 2010 runs as of May 2010"
    echo "         --egamma-G ............ standard egamma period G"
    echo "         --egamma-2011 ......... standard egamma for 2011"
    echo "         --egamma-2012 ......... standard egamma for 2012"
    echo "         -l <last_n_runs> ...... "
    echo "         -n <n_events> ......... "
    echo "         -p <project_tag> ...... "
    echo "         -r <run> .............. "
    echo "         -s <show_condition> ... "
    echo "         -t <time> ............. "
}

args=(`getopt -l gr2009,egamma-G,egamma-2012,dq= l:r:t:n:p:s:L:H:R:h $*`)
# set -- $args

# while getopts l:r:t:n:p:s:L:H:R:h opt $*; do
while [[ $# -ge 1 ]]; do

    opt=$1;
    OPTARG=$2;
    echo "opt = $opt"
    case $opt in 
	"-l") # recent <N> runs
	    addFindCond "run last $OPTARG"
	    shift;;
	"-r")
	    addFindCond "run $OPTARG"
	    shift 2;;
	"-t")
	    addFindCond "time last $OPTARG"
	    shift 2;;
	"-n")
	    addFindCond "ev $OPTARG"
	    shift 2;;
	"-p")
	    addFindCond "ptag $OPTARG"
	    shift 2;;
	"-s")
	    s_show=`echo $OPTARG | sed "s/,/ and /g"`
	    lock_show=yes
	    shift 2;;
	"--dq")
	    addFindCond "dq $OPTARG"
	    shift 2;;
	"-L")
	    addFindCond "run last $OPTARG";
	    addShowCond "run and events and t and ptag"
	    shift;;
	"-H")
	    addFindCond "time last $OPTARG";
	    addShowCond "run and events and t and ptag"
	    shift;;
	"-R")
	    addFindCond "run $OPTARG";
	    addShowCond "run and events and t and st"
	    shift;;
	"--gr2009")
	    s_find="run 141000+ and dq lar,pix,sct,trtb,trte y+ and dq atlsol,atltor g and mag s and lhc beamenergy 449+"
	    s_show="run and ptag and events and t"
	    shift;;
	"--gr2010-04")
	    s_find="run 140000+ and ptag data10_7TeV and ev 1000+ and dq lar,pix,sct y+ and dq atlsol,atltor g and mag s"
	    s_show="run and ptag and events and t"
	    shift;;
	"--gr2010-05")
	    s_find="run 140000+ and ptag data10_7TeV and ev 1000+ and dq lar,pix,sct,trtb,trte y+ and dq atlsol,atltor g and mag s"
	    # s_find="run 140000+ and ptag data10_7TeV and ready and dq atlgl g and dq cp_eg_electron_barrel y+ and dq cp_eg_electron_endcap y+ and dq tigb g"
	    s_show="run and ptag and events and t and ready"
	    shift;;
	"--egamma-G")
	    pass1="LBSUMM#DetStatus-v03-pass1-analysis-2010G"
	    addFindCond "partition ATLAS and db DATA"
	    addFindCond "lhc stablebeams T and ptag data10_7TeV and ready"
	    #addFindCond "dq ATLGL $pass1 g"
	    #addFindCond "dq L1CTP $pass1 g"
	    #addFindCond "dq cp_eg_electron_barrel $pass1 g"
	    #addFindCond "dq cp_eg_electron_endcap $pass1 g"
	    shift;;
	"--egamma-2011")
	    #addFindCond "partition ATLAS and db DATA"
	    #addFindCond "lhc stablebeams T and ptag data11_7TeV and ready"
	    addFindCond "ptag data11_7TeV and ready"
	    #addFindCond "dq ATLGL $pass1 g"
	    #addFindCond "dq L1CTP $pass1 g"
	    #addFindCond "dq cp_eg_electron_barrel $pass1 g"
	    #addFindCond "dq cp_eg_electron_endcap $pass1 g"
	    shift;;
	"--egamma-2012")
	    addFindCond "ptag data12_8TeV and ready"
	    shift;;
	"-h")
	    usage $0;
	    exit 0
	    break;;
    esac
    shift;
done


if [[ $s_find == "" ]]; then
    echo "No find condition specified, using default"
    s_find="run 139545+ and ev 100k+"
fi
if [[ $s_show == "" ]]; then
    echo "No show condition specified, using default"
    s_show="run and events and t and ptag"
fi

arg="find $s_find / show $s_show"
echo "Execute AtlRunQuery '$arg' ..."
python `which AtlRunQuery.py` $arg


