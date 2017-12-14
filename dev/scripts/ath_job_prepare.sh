#!/usr/local/bin/zsh

input_filelist=""
prefix="filelist_"
castor_dir=""
data_dir=""
work_dir="."
jobconf="jobconf.txt"
jobconf_temp=`pwd`/"jobconf.txt_temp"

function usage() {
    echo "Usage: $1 [options]"
    echo "Options: -F ... file list []"
    echo "         -p ... prefix [$prefix]"
    echo "         -c ... castor directory []"
    echo "         -d ... data directory []"
    echo "         -w ... working directory [.]"
}

while getopts :F:p:c:d:w:j: opt; do
    case $opt in
	"F") # file list
	    input_filelist=$OPTARG;;
	"p") # prefix
	    prefix=$OPTARG;;
	"c") # CASTOR path
	    castor_dir=$OPTARG;;
	"d") # Data directory path
	    data_dir=$OPTARG;;
	"j") # jobconf file
	    jobconf=$OPTARG;;
	"w") # Working directory
	    work_dir=$OPTARG;;
    esac
done

filepath=""
if [[ $input_filelist == "" ]]; then
    usage $0;
    exit 1
else;
    if [[ $data_dir != "" ]]; then
	data_dir=`echo $data_dir | sed -f $TK_ROOT/share/slash_to_backslashslash.sed`
	filepath="$data_dir"
    fi
    if [[ $castor_dir != "" ]]; then
	castor_dir=`echo $castor_dir | sed -f $TK_ROOT/share/slash_to_backslashslash.sed`
	filepath="$castor_dir"
    fi
fi

# exit 0

function begin_hook() {
    echo "$1_begin"
}
function end_hook() {
    echo "$1_end"
}
function add_hook() {
    hook=$1
    begin_hook $hook
    for ((i=2; $i<=$#; i=$i+1)); do
	cmd=$*[$i]
	eval "args=( $cmd )"
	cmd=($args[1])
	args=$args[2,${#args}]
	# execute the command
	$cmd $args
    done
    end_hook $hook
}

function prepare_job() {
    jobid=$1;
    inputlist=$2;

    echo "Preparing job $jobid ..."

    mkdir -p $jobid
    cd $jobid
    hookfile=hooks.txt
    if [[ -e $hookfile ]]; then
	mv $hookfile $hookfile.sav
    fi
# input_files
    ( # InputFiles
	begin_hook "#JO-HOOK-InputFiles";
	echo "InputFiles=[";
	cat $inputlist | sed "s/^/  '$filepath\//" | sed "s/$/',/" ;
	echo "]";
	echo "EvtMax = -1"
	end_hook "#JO-HOOK-InputFiles"
    ) >> $hookfile
    if [[ -e $jobconf_temp ]]; then
	( # JobID
	    begin_hook "#SCRIPT-HOOK-JobID"
	    echo "JobID=$jobid"
	    end_hook "#SCRIPT-HOOK-JobID"
	) >> $hookfile
	( # JobOptionsFile
	    begin_hook "#SCRIPT-HOOK-JobOptionsFile"
	    a=`grep jobOptions_file $jobconf_temp| sed "s/=/ = /"`
	    a=(`echo $a | sed "s/<-[^<]\+//"`)
	    echo "JobOptionsFile=$a[3,-1]"
	    end_hook "#SCRIPT-HOOK-JobOptionsFile"
	) >> $hookfile
	( # PackageTarFile
	    begin_hook "#SCRIPT-HOOK-PackageTarFile"
	    a=`grep package_tar $jobconf_temp| sed "s/=/ = /"`
	    echo "package_tarfile=$a[3,-1]"
	    end_hook "#SCRIPT-HOOK-PackageTarFile"
	) >> $hookfile
	( # JobType
	    begin_hook "#SCRIPT-HOOK-JobType"
	    a=(`grep job_type $jobconf_temp | sed "s/=/ = /"`)
	    echo "JobType=$a[3,-1]"
	    end_hook "#SCRIPT-HOOK-JobType"
	) >> $hookfile
	( # JobInputFiles
	    begin_hook "#SCRIPT-HOOK-JobInputFiles"
	    a=(`grep job_input_file $jobconf_temp | sed "s/=/ = /"`)
	    echo "JobInputFiles=($a[3,-1])"
	    end_hook "#SCRIPT-HOOK-JobInputFiles"
	) >> $hookfile
	( # CMTTAG
	    begin_hook "#SCRIPT-HOOK-CMTTAG"
	    a=(`grep cmttag $jobconf_temp | sed "s/=/ = /"`)
	    echo "$a[1]=$a[3,-1]"
	    end_hook "#SCRIPT-HOOK-CMTTAG"
	) >> $hookfile
    fi
    mv $hookfile ${hookfile}_tmp
    cat ${hookfile}_tmp | sed "s/'\/castor/'castor:\/castor/" > $hookfile
    # cat ${hookfile}_tmp > $hookfile
    rm ${hookfile}_tmp
    cd -
}


#-------------------------------------------------------------------------
# Start of the main script
#-------------------------------------------------------------------------
cur_dir=`pwd`
cd $work_dir
#----------------------------------------
# take log of how the jobs were prepared
rm -fr job_prep.out
echo "Job prepared from directory: $cur_dir" >> job_prep.out
echo "Command: $0 $*" >> job_prep.out
#----------------------------------------
# if [[ $input_filelist[1] != '/' ]]; then
#     input_filelist="../$input_filelist"
# fi
split -d -l 10 $input_filelist $prefix
lists=(`ls -1 $prefix*`)

joblist=()
for f in $lists; do
    new_id=`echo $f | sed "s/$prefix\([0-9]\+\)/\1/"`
    joblist=($joblist $new_id)
    rm -f tmp
done
echo $joblist

if [[ -e joblist ]]; then
    mv joblist joblist.sav
fi
# jc_read.py $jobconf > $jobconf_temp
for job in $joblist; do
    prepare_job $job `pwd`/$prefix$job
    echo $job >> joblist
done
# rm $jobconf_temp
echo "A list of job IDs stored in file 'joblist'"

mkdir -p filelists
mv $lists[@] filelists

cd $cur_dir

