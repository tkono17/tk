#!/usr/bin/env zsh

joboptions_base=""
joblist_file="joblist"
work_dir="."
extra_script=""
output_file="job_run.out"
jo_tag="^#JO-HOOK"
athena_opt=""

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
my_joboptions="athena_joboptions.py"

function usage() {
    echo "Usage: $1 [options]"
    echo "------"
    echo "Options: -j <joboption_base> ... base jobOptions file"
    echo "         -l <joblist_file>   ... joblist file [joblist]"
    echo "         -e <extra_script>   ... extra setup script for a job [""]"
    echo "         -w <work_dir>       ... working directory [.]"
    echo "         -o <output_file>    ... output file [job_run.out]"
    echo "         -t <jo_tag>         ... tag prefix for inserting JO frag."
}

function abspath() {
    if [[ $# -ne 1 ]]; then
	echo ""
    else;
	cur_dir=`pwd`
	dir=`dirname $1`
	name=`basename $1`
	cd $dir;
	echo `pwd`/$name
	cd $cur_dir
    fi
}

while getopts :j:l:e:w:o: opt; do
    case $opt in
	"j") # Base joboptions flie
	    joboptions_base=$OPTARG;
	    ;;
	"l") # joblist file
	    joblist_file=$OPTARG
	    ;;
	"e")
	    extra_script=$OPTARG
	    ;;
	"w")
	    work_dir=$OPTARG
	    work_dir=`abspath $work_dir`
	    ;;
	"o")
	    output_file=$OPTARG
	    ;;
	"t")
	    jo_tag=$OPTARG
	    ;;
    esac
done
joboptions_base=`abspath $joboptions_base`
joblist_file=`abspath $joblist_file`
extra_script=`abspath $extra_script`
output_file=`abspath $output_file`

if [[ $joboptions_base == "" ]]; then
    usage $0
    exit 1
fi

function setup() {
    cur_dir=`pwd`
    if [[ $# -eq 1 ]]; then
	jobid=$1
	cd $jobid
    fi
    # ln -s $joboptions_base .
    if [[ ${extra_script} != "" && -e ${extra_script} ]]; then
	source ${extra_script}
    fi
    joboptions_base2=`basename $joboptions_base`
    insert_in_tag.py -t $jo_tag $joboptions_base ${my_joboptions} hooks.txt
    cd $cur_dir
}

function run_job() {
    cur_dir=`pwd`
    if [[ $# -eq 1 ]]; then
	jobid=$1;
	cd $jobid
    fi
    echo "Running job $job ..." >> $output_file
    athena.py ${athena_opt} ${my_joboptions} >& a.log
    cd $cur_dir
}

function run_jobs() {
    cur_dir=`pwd`
    cd $work_dir
    joblist=(`cat $joblist_file|grep -v "^#"`)
    for job in $joblist; do
	setup $job
	run_job $job
    done
    cd $cur_dir
}

cur_dir=`pwd`
rm -f $output_file
(
    echo "Job started on: "`date`;
    echo "Job running from directory: $cur_dir";
    echo "Command: $0 $*";
    echo "*** TestArea: ";
    echo "$TestArea";
    echo "CMT path:";
    cmt show path;
) >> $output_file

run_jobs

echo "Job ended on: "`date` >> $output_file


