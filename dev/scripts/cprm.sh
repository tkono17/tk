#!/usr/bin/env zsh

src_dir=""
dest_dir=""
do_loop="no";
(( sleep_time=60 ))
ignore_pattern=""
select_pattern=""
donot_copy="no"
verbose="no"
do_delete="yes"

function usage() {
    echo "Usage: $1 [options] <src_dir> <dest_dir>"
    echo "  Copies all files under <src_dir> to <dest_dir>"
    echo "Options: -r <sleep_time> ... Run in an infinite loop call itself"
    echo "                             every <sleep_time> seconds"
    echo "         -i <pattern>    ... Ignore files with <pattern> (using ls)"
    echo "         -s <pattern>    ... Select files with <pattern> (using ls)"
    echo "         -n              ... No real action"
    echo "         -v              ... Verbose mode"
    echo "         -k              ... Do not delete the file after copying"
    echo "Examples: "
    echo "  o Copy all files in current directory to \$HOME"
    echo "    > $1 . \$HOME"
    echo "  o Copy all files in directory A ending with '.root' to \$HOME"
    echo "    > $1 -s \"\.root$\" A \$HOME"
    echo "  o Run above repeatedly by checking the availability the input "
    echo "    files every 60 seconds"
    echo "    > $1 -l 60 -s \"\.root$\" A \$HOME"
}

function cprm() {
    files=(`ls -1 $src_dir`)
    if [[ $select_pattern != "" ]]; then
	files=(`echo $files |sed "s/[[:space:]]/\n/g" |grep "$select_pattern"`)
    fi
    if [[ $verbose == "yes" ]]; then 
	ff=$(echo $files |sed "s/[[:space:]]/\n/g")
	echo "*** Files before filter : \n$ff"
    fi
    if [[ $ignore_pattern != "" ]]; then
	ff=$files
	files=(`echo $ff|sed "s/[[:space:]]/\n/g"|grep -v "$ignore_pattern"`)
    fi
    if [[ $verbose == "yes" ]]; then
	ff=$(echo $files |sed "s/[[:space:]]/\n/g")
	echo "*** Files after filter : \n$ff"
    fi
    if [[ $#files -gt 0 ]]; then
	for file in $files; do
	    if [[ -f $src_dir/$file ]]; then
		if [[ $donot_copy == "yes" ]]; then
		    echo "Not doing 'cp $src_dir/$file $dest_dir/$file'"
		    continue
		fi
		cp $src_dir/$file $dest_dir/$file;
		if [[ $? == 0 ]]; then
		    if [[ $do_delete == "yes" ]]; then
			rm $src_dir/$file;
		    fi
		    echo "Successfully copied file $file to $dest_dir"
		else
		    echo "Error while copying file $file"
		fi
	    fi
	done
    fi
}

if [[ $# -lt 2 ]]; then
    usage $0;
    exit 1;
fi

((first_arg=1))
while getopts :r:i:s:nvk opt; do
    case $opt in
	"r")
	    do_loop="yes";
	    (( sleep_time=$OPTARG))
	    (( first_arg = $OPTIND));;
	"i")
	    ignore_pattern=$OPTARG
	    (( first_arg = $OPTIND));;
	"s")
	    select_pattern=$OPTARG
	    (( first_arg = $OPTIND));;
	"n")
	    donot_copy="yes"
	    (( first_arg = $OPTIND + 1));;
	"v")
	    verbose="yes"
	    (( first_arg = $OPTIND + 1));;
	"k")
	    do_delete="no"
	    (( first_arg = $OPTIND + 1));;
	"?")
	    echo "Warning: Invalid option '$OPTARG'";;
	":")
	    echo "Warning: Option '$OPTARG' is missing an argument";;
	*)
	    echo "Unknown option $opt";;
    esac
done

src_dir=$argv[$first_arg]
(( first_arg = $first_arg + 1 ))
dest_dir=$argv[$first_arg]

#echo "src_dir=$src_dir"
#echo "dest_dir=$dest_dir"
#echo "do_loop=$do_loop"
#echo "sleep_time=$sleep_time"
#echo "ignore pattern=$ignore_pattern"

echo "Copy all files in $src_dir to $dest_dir"
if [[ $select_pattern != "" ]]; then
    echo "... selecting files with pattern $select_pattern"
fi
if [[ $ignore_pattern != "" ]]; then
    echo "... ignoring files with pattern $ignore_pattern"
fi

if [[ $do_loop == "yes" ]]; then
    echo "run every $sleep_time seconds"
    while [[ "0" == "0" ]]; do
	cprm;
	sleep $sleep_time;
    done
else
    cprm;
fi
echo "done"

