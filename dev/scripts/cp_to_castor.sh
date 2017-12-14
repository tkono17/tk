#!/usr/local/bin/zsh

# dataset="caldigoff1_mc12.007210.singlepart_mu9.digit.RDO.v12003107"
# dataset="caldigoff1_mc12.007223.singlepart_mu28.digit.RDO.v12003107"

data_dir=".";
castor_dir="/castor/cern.ch/user/t/tkohno";

input_list="";
files=(`cat $input_list`)

echo "Number of files to copy: ${#files}"

for file in $files; do
    echo "Processing file : $file"
    rfcp $data_dir/$file $castor_dir
done
