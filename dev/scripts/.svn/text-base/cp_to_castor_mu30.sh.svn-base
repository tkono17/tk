#!/usr/local/bin/zsh

# dataset="caldigoff1_mc12.007210.singlepart_mu9.digit.RDO.v12003107"
# dataset="caldigoff1_mc12.007223.singlepart_mu28.digit.RDO.v12003107"
dataset="caldigoff1_mc12.007224.singlepart_mu30.digit.RDO.v12003107"

data_dir="/space/tkohno/data/castor_work/${dataset}"
castor_dir="/castor/cern.ch/user/m/muonprod/1203/digit/${dataset}"

tmp_files_to_copy=/tmp/files_to_copy.txt
rm -f $tmp_files_to_copy
ls -1 ${data_dir} | grep ".root" > $tmp_files_to_copy
files=(`cat /tmp/files_to_copy.txt`)

echo "nfiles: ${#files}"


for file in $files; do
    echo "Processing file : $file"
    rfcp $data_dir/$file $castor_dir
done
