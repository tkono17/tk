#----------------------------------------------------------------------------
# source it
#----------------------------------------------------------------------------

do_list=no
do_help=no
project_name=all

getopt p:lah $*;


AFSHOME=/afs/cern.ch/user/t/tkohno
athenadir=/rscratch/pcatr18/tkohno/athena
rel=

while [[ $# -ge 1 ]]; do
    opt=$1;
    OPTARG=$2;
    echo "opt=$opt"
    case $opt in 
	-p)
	    project_name=$OPTARG
	    shift;;
	-a)
	    project_name=all
	    shift 2;;
	-d)
	    athenadir=$OPTARG
	    shift 2;;
	-l) 
	    do_list=yes
	    shift;;
	-r)
	    rel=$OPTARG
	    shift 2;;
	-h)
	    do_help=yes
	    shift;;
	*)
	    shift;;
    esac
done


typeset -A nightlyTags
cmn=oneTest,opt,32,runtime
if [[ $rel != '' ]]; then
    cmn=${cmn},${rel}
fi

nightlyTags=(
    bugfix
    bugfix,${cmn}

    bugfix-val
    bugfix,val,${cmn}

    15.6.X-VAL
    15.6.X-VAL,${cmn}

    dev
    dev,${cmn}

    devval
    devval,${cmn}

    prod-15.6.3.Y
    AtlasProduction,15.6.3.Y,${cmn}
    
    prod-15.6.6.Y
    AtlasProduction,15.6.6.Y,${cmn}
    
    prod-15.6.X.Y
    AtlasProduction,15.6.X.Y,${cmn}

    prod-16.0.X.Y
    AtlasProduction,16.0.X.Y,${cmn}

    prod-16.0.X.Y-VAL
    AtlasProduction,16.0.X.Y-VAL,${cmn}

    prod-16.0.2.5
    AtlasProduction,16.0.2.5,${cmn}

    prod-15.6.X.Y-VAL
    AtlasProduction,15.6.X.Y-VAL,${cmn}

    p1hlt-15.6.9.17
    AtlasP1HLT,15.6.9.17,${cmn}

    p1hlt-15.6.9.28
    AtlasP1HLT,15.6.9.28,${cmn}

    p1hlt-15.6.9.29
    AtlasP1HLT,15.6.9.29,${cmn}

    p1hlt-15.6.9.37
    AtlasP1HLT,15.6.9.37,${cmn}

    p1hlt-15.5.X.Y
    AtlasP1HLT,15.5.X.Y,${cmn}
    
    p1hlt-15.6.X.Y
    AtlasP1HLT,15.6.X.Y,${cmn}

    p1hlt-15.6.X.Y-VAL
    AtlasP1HLT,15.6.X.Y-VAL,${cmn}

    cafhlt-15.6.9.28.1
    AtlasCAFHLT,15.6.9.28.1,${cmn},slc5,gcc43

    cafhlt-15.6.9.29.1
    AtlasCAFHLT,15.6.9.29.1,${cmn},slc5,gcc43

    cafhlt-15.6.9.36.2
    AtlasCAFHLT,15.6.9.36.2,${cmn},slc5,gcc43

    cafhlt-15.6.X.Y.Z-menu
    AtlasCAFHLT,15.6.X.Y.Z,${cmn},slc5,gcc43

    cafhlt-15.6.X.Y.Z
    AtlasCAFHLT,15.6.X.Y.Z,${cmn},slc5,gcc43

    cafhlt-15.6.X.Y.Z-VAL
    AtlasCAFHLT,15.6.X.Y.Z-VAL,${cmn},slc5,gcc43
)


function setup() {
    k=$1
    tag=$nightlyTags[$k];
    cd $athenadir
    echo "$k ==> $tag"
    mkdir -p $k; mkdir -p $k/run
    cd $k
    source $AFSHOME/cmthome/setup.sh -tag="${tag}"
    cd $athenadir/$k
}

if [[ $project_name == "all" ]]; then
    for k in ${(k)nightlyTags}; do
	setup $k
    done
elif [[ $project_name != "" ]]; then
    k=$project_name;
    p=$nightlyTags[$project_name];
    if [[ $p != "" ]]; then
	setup $k
    else
	echo "Unknown project name: $project_name"
    fi
fi


