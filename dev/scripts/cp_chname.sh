#!/usr/bin/env zsh
#----------------------------------------------------------------------
# cp_chname.sh
#-------------
# Copy files of the same name in several directories to one directory
# while changing the name of each file to have different names
# For example:
#  dir1/[0-9]/a.root -> dir2/a_[0-9].root
#----------------------------------------------------------------------

# src_files=${HOME}/gangadir/workspace/Local/85/*/output/muontest.root
# dest_dir=/space2/tkohno/data/Zmunu/PythiaZmumu/ROOT
dest_dir=/space2/tkohno/data/Zmunu/PythiaZmumu/ROOT

# all_files=(`ls $src_files`)
# all_files=(`ls ${HOME}/gangadir/workspace/Local/85/*/output/muontest.root`)
# all_files=(`ls /space2/tkohno/data/single_mu/kiyamuraAOD/mu19/mu19.*/aan.root`)
all_files=(`ls /space2/tkohno/data/P1commissioning/m4/20895/*/ntuple.root`)
for f in $all_files; do
    echo $f
    key=`echo $f|sed "s/[\/[:alnum:]]\+\/20895\/\([[:digit:]]\+\)\/ntuple.root/\1/"`
    f2="m4_20895_$key.root"
    echo "Copying $f to $f2"
    cp $f  $f2
done
