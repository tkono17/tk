#!/usr/bin/env zsh

function usage() {
    echo "Usage: $0 <dq2_ls_f_output> <filetype> <nfiles=-1>"
    echo "------"
    echo "Example: $0 filelist.txt AANT -1"
    echo "         filelist.txt: Output of dq2-ls -f <dataset>"
    echo "         AANT        : Pattern match for files to copy"
    echo "         nfiles      : Number of files to copy"
    echo ""
}


filelist=''
filetype=''
nfiles=-1

if [[ ${#@} -ne 2 && ${#@} -ne 3 ]]; then
    usage;
    exit 1
else;
    filelist=$1;
    filetype=$2;
    if [[ ${#@} -ge 3 ]]; then
	nfiles=$3;
    fi
fi

tmpfile="tmptmp"
if [[ -e $tmpfile ]]; then
    rm -f $tmpfile;
fi

dataset=`grep -v '^$' $filelist |head -1`
grep -v '^$' $filelist | grep '\[' | cut -c 4- | \
    sed "s/\t/ /g" |grep $filetype | cut -d ' ' -f 2 > $tmpfile
files=(`cat $tmpfile`)

i=0
first=yes
# cat $tmpfile
echo "dataset: $dataset (${#files} files)"

for f in $files; do
#    if [[ $first == yes ]]; then
#	# ignore the first line of the file which is just the dataset name
#	first=no
#	continue
#    fi
    if [[ $i -eq $nfiles ]]; then
	echo "Number of files reached the specified maximum ($nfiles)"
	break;
    fi
    (( i = $i + 1 ))
    if [[ -e $f ]]; then
	echo "File $f already exists"
    else;
	dq2get=dq2-get
	domain=`hostname -d`
	if [[ $domain == 'naf' ]]; then
	    #dq2get=dq2-get-naf
	fi
	echo "Executing $dq2get -D -f $f $dataset ..."
	$dq2get -D -f $f $dataset
    fi
done

