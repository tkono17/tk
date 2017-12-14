#!/usr/bin/env zsh
#----------------------------------------------------------------------
# This script submits pathena job given an input dataset and jobOptions
# The name of the output dataset is deduced from the input dataset as
# something like 
# outDS=user.tkohno.data.${jo}.${inDS}.${release}.${version}
#----------------------------------------------------------------------

jo=$TestArea/TkAthena/AnalysisJobs/TrigJob/share/testAodToNtupleRel156.py
release=$AtlasVersion
version=v2
# site=DESY-HH
site=
cloud=
destSE=
nFilesPerJob=5
nGBPerJob=
tkdir=user.tkohno.data
#dbRelease=LATEST
dbRelease=

#----------------------------------------------------------------------
# Options
#----------------------------------------------------------------------
job_name=
dataset_definition=datasets.sh
dataset_definition=
ds_alias=
jo=
do_list_datasets=no
do_merge=no
do_help=no
do_submit=yes
do_find_replicas=no
output_log='panda_submit.log'
append_log=no

cmdargs=($0 $@)
function shortName() {
    echo $1 | sed "s/\(AOD\|ESD\|RAW\).*/\1/g";
}

function exec_and_save() {
    ddd=`pwd`
    echo "Executing $1 ... from directory ${ddd}";
    echo $*;
    $*;
}

function check_submit() {
    job_out=$1
    job_err=$2
    njobs=`grep JobsetID $job_out | wc -l`
    jobid=`grep JobsetID $job_out | head -1`
    if [[ $njobs -gt 0 ]]; then
	echo " ==> Successfully submitted pathena job : $jobid" >> $output_log
	echo "     SUBMITTED: "`pwd` >> $output_log
    else
	echo " ==> *** ERROR: Could not submit pathena job" >> $output_log
	echo "     NOT_SUBMITTED: "`pwd` >> $output_log
	grep -i error $job_out $job_err
    fi
    echo "# Done checking submit"
}

function job_submit() {
    jname=$1
    inDS=$2
    inDS2=`shortName $inDS`
    if [[ $# -ge 3 ]]; then
	inDS2=$3
    fi
    workdir=$jname
    jobtype=$job_name
    if [[ $jobtype == "" ]]; then
	jobtype=`basename $jo | sed "s/\.py//" | sed "s/^test//"`
    else
	workdir=${job_name}.${jname}
    fi
    outDS=${tkdir}.${jobtype}.${inDS2}.${release}.${version}

    mkdir -p $workdir/run
    if [[ $workdir == "" ]]; then
    elif [[ ! -d $workdir ]]; then
	echo "Directory $jname does not exist, first create it by hand!"
    else
	echo "Submitting pathena job $jname ..." >> $output_log
	cd $workdir/run
	job_out=`pwd`/job_sub.out
	job_err=`pwd`/job_sub.err
#----------------------------------
	command="pathena"
        # command="echo"
	command=($command $jo --inDS ${inDS} --outDS ${outDS})
	if [[ $site != "" ]]; then
	    command=($command --site $site)
	fi
	if [[ $cloud != "" ]]; then
	    command=($command --cloud $cloud)
	fi
	if [[ $nFilesPerJob != "" ]]; then
	    command=($command --nFilesPerJob $nFilesPerJob)
	fi
	if [[ $nGBPerJob != "" ]]; then
	    command=($command --nGBPerJob $nGBPerJob)
	fi
	if [[ $dbRelease != "" ]]; then
	    command=($command --dbRelease $dbRelease)
	fi
	if [[ $destSE != "" ]]; then
	    command=($command --destSE $destSE)
	fi
#----------------------------------
	if [[ $do_submit == yes ]]; then
	    exec_and_save $command 1>$job_out 2>$job_err;
	    if [[ -e $job_out ]]; then
		echo "Check log files after submit"
		check_submit $job_out $job_err
		cat $output_log
		echo "Dumped log"
	    fi
	else
	    # echo panda_submit.sh $opts
	    echo $command
	fi
	cd -
    fi
    echo "Submitted pathena job with the following command:" >> $job_out
    echo $cmdargs >> $job_out
}

function usage() {
    cmd=`basename $1`
    echo "Usage: $cmd [options]
--------
Options:
-d|--dataset-definition <file> ... File with dataset definition (alias->DS map)
-k|--keys <ds_alias> ............. Dataset alias defined in the definition file
                                   (separate by commas if more than 1)
-l|--list-datasets ............... List available alias->Datasets
-m|--merge ....................... Merge all datasets in one job
                                   (-l option will be ignored)x
-n|--nFilesPerJob <n> ............ Number of input files per job
--nGBPerJob <MaxGB> .............. Maximum disk space (GB)
-j|--jobOptions <file> ........... Job options file
--jobName <name> ................. Job name (will be used in outDS name)
--append-log ..................... Append submit log into an existing file
-c|--cloud <cloud> ............... Cloud (DE, FR, ...)
-s|--site <site> ................. Grid site to submit the job
--destSE <destSE> ................ Destination SE (e.g. DESY-HH_LOCALGROUPDISK)
-q|--quite ....................... Be quiet, i.e don't actually submit the job
-v|--version <version> ........... Version of this type of grid job
-h|--help ........................ Help
---------
Examples:
---------
$cmd -d datasets.sh -k 7TeV_PythiaZee,7TeV_PythiaWenu -j jo.py
$cmd -d datasets.sh -l
"
}

#----------------------------------------------------------------------
# Parse options
#----------------------------------------------------------------------
cmd=$0
# args=(`getopt d:k:n:j:lmrc:s:v:h $*`)
while [[ $# -ge 1 ]]; do
    opt=$1
    OPTARG=$2
    case $opt in
	-d|--dataset-definition)
	    dataset_definition=$OPTARG
	    shift 2;;
	-k|--key)
	    ds_alias=$OPTARG
	    shift 2;;
	-j|--jobOptions)
	    jo=$OPTARG
	    shift 2;;
	--jobName)
	    job_name=$OPTARG
	    shift 2;;
	--append-log)
	    append_log=yes
	    shift 1;;
	-l|--list-datasets)
	    do_list_datasets=yes
	    shift 1;;
	-n|--nFilesPerJob)
	    nFilesPerJob=$OPTARG
	    shift 2;;
	--nGBPerJob)
	    nGBPerJob=$OPTARG
	    shift 2;;
	-v|--version)
	    version=$OPTARG
	    shift 2;;
	-c|--cloud)
	    cloud=$OPTARG
	    shift 2;;
	-s|--site)
	    site=$OPTARG
	    shift 2;;
	--destSE)
	    destSE=$OPTARG;
	    shift 2;;
	-r|--replicas)
	    do_find_replicas=yes
	    shift 1;;
	-q|--quite)
	    do_submit=no
	    shift 1;;
	-m|--merge)
	    do_merge=yes
	    shift 1;;
	-h|--help)
	    do_help=yes
	    shift 1;;
	*)
	    shift 1;
    esac
done

#----------------------------------------------------------------------
# Main program
#----------------------------------------------------------------------
if [[ $do_help != no ]]; then
    usage $cmd
    exit 0
fi
if [[ -e $dataset_definition ]]; then
    source $dataset_definition
    if [[ $ds_alias == "ALL" ]]; then
	ds_alias=($keys)
    fi
    if [[ $do_merge == 'yes' ]]; then
	tmp=(`echo ${(k)datasets} |sed "s/ /\n/g" | sort`)
	k=merge.${tmp[1]}-${tmp[-1]}
	v=(`echo ${datasets} | sed "s/ /,/g"`)
	datasets+=($k $v)
	ds_alias=($k)
    fi
else
    usage $cmd
    exit -1
fi

if [[ $do_list_datasets != no ]]; then
    echo "Datasets defined :"
    for k in $keys; do
	echo "$k\n   => $datasets[$k]"
    done
    exit 0
fi
if [[ $do_find_replicas == yes ]]; then
    for k in $keys; do
	dq2-ls -r $datasets[$k]
    done
    exit 0
fi

if [[ -e $jo ]]; then
    if [[ $jo[0] != '/' ]]; then
	dir=`dirname $jo`
	bname=`basename $jo`
	cd $dir;
	jo=`pwd`/$bname
	cd -
    fi
else
    echo "***Warning: JobOptions file '$jo' does not exist, now in `pwd`"
    exit 1
fi

if [[ ${append_log} == 'no' && -e $output_log ]]; then
    rm $output_log
fi
output_log=`pwd`/$output_log
echo "JobName: ${job_name}" >> $output_log
echo "JobOptions: ${jo}" >> $output_log

#echo $ds_alias | sed "s/,/ /g"
ds_aliases=(`echo $ds_alias | sed "s/,/ /g"`)
for dsAlias in $ds_aliases; do
    if [[ $dsAlias != "" ]]; then
	ds=$datasets[$dsAlias]
	if [[ $ds != "" ]]; then
	    if [[ $do_merge == yes ]]; then
		job_submit $dsAlias $ds $dsAlias
	    else
		echo "Submit pathena job for $dsAlias ..."
		job_submit $dsAlias $ds
		echo "Done"
	    fi
	else
	    echo "***Warning: Dataset alias '$dsAlias' is not defined."
	    echo "   Try '`basename $cmd` -d $dataset_definition -l' to find out which datasets are defined"
	fi
    fi
done

if [[ -e $output_log ]]; then
    cat $output_log
fi

# jsub ddd

