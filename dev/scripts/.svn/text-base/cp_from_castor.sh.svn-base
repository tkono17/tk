#!/usr/bin/env zsh

# dataset="caldigoff1_mc12.007210.singlepart_mu9.digit.RDO.v12003107"
# dataset="caldigoff1_mc12.007223.singlepart_mu28.digit.RDO.v12003107"

data_dir=".";
castor_dir="";
input_list="";

function usage() {
    echo "Usage: $1 -d <local_dir> -c <castor_dir> [-l <input_list>|-f <file>]"
}

if [[ $# -ne 6 ]]; then
    usage $0;
    exit 1;
fi

while getopts :c:d:l: opt; do
    case $opt in 
	"c")
	    castor_dir=$OPTARG;;
	"d")
	    data_dir=$OPTARG;;
	"l") 
	    input_list=$OPTARG;;
    esac
done

echo "<data_dir>=$data_dir"
echo "<castor_dir>=$castor_dir"
echo "<input_list>=$input_list"

files=(`cat $input_list|grep -v '^#'`)

echo "Number of files to copy: ${#files}"

for file in $files; do
    echo "Processing file : $file"
    if [[ -e $data_dir/$file ]]; then
	echo "File $data_dir/$file already exists."
    else;
	rfcp $castor_dir/$file $data_dir/${file}.copying
	mv $data_dir/${file}.copying $data_dir/$file
    fi
done
