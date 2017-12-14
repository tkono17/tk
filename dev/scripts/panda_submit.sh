#!/usr/bin/env zsh

function usage() {
    echo "Usage: $1 -j <jobOptions> -i <inDS> -o <outDS> [options]"
    echo "-----"
    echo "Options: -s <site> ......... Grid site"
    echo "         -n <N> ............ Number of files per job"
    echo "         -d <dbRelease> .... DBRelease (Dataset:Filename)"
    echo "         -h ................ Help"
}

function exec_and_save() {
    ddd=`pwd`
    echo "Executing $1 ... from directory ${ddd}";
    echo $*;
    $*;
}

job_config=""
inDS=''
outDS=''
site=''
cloud=''
n_files_per_job=10

if [[ $# == 0 ]]; then
    usage $0
    exit 1
fi

while getopts j:i:o:c:d:s:n:h opt $*; do
    case $opt in 
	"j") job_config=$OPTARG;;
	"i") inDS=$OPTARG;;
	"d") dbRelease=$OPTARG;;
	"o") outDS=$OPTARG;;
	"c") cloud=$OPTARG;;
	"s") site=$OPTARG;;
	"n") n_files_per_job=$OPTARG;;
	"h")
	    usage $0
	    exit 0;;
    esac
done

package_abspath=`pwd`/..

if [[ $job_config == "" || $inDS == "" || $outDS == "" ]]; then
fi
if [[ ! -e $job_config ]]; then
    echo "Athena job options file $job_config does not exist";
    exit -1
fi

job_out=`pwd`/job_sub.out
job_err=`pwd`/job_sub.err

job_config_abspath=${job_config}
if [[ $job_config[0] != "/" ]]; then
    job_config_abspath=`pwd`/${job_config}
fi
if [[ -d ${package_abspath} && -d ${package_abspath}/run ]]; then
    cd $package_abspath/run;
    cp $job_config_abspath .
    jobOptions=`basename $job_config_abspath`
    echo "Running ... " 
    command="pathena"
    # command="echo"
    command=($command $jobOptions --inDS ${inDS} --outDS ${outDS})
    if [[ $site != "" ]]; then
	command=($command --site $site)
    fi
    if [[ $cloud != "" ]]; then
	command=($command --cloud $cloud)
    fi
    if [[ $n_files_per_job != "" ]]; then
	command=($command --nFilesPerJob $n_files_per_job)
    fi
    if [[ $dbRelease != "" ]]; then
	command=($command --dbRelease $dbRelease)
    fi
    exec_and_save $command 1>$job_out 2>$job_err;
    cd -;
else
    echo "No directory ${package_abspath}/run found";
    exit -1;
fi

