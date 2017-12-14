#!/usr/bin/env zsh

gangadir=~/gangadir
job_name=14

cd $gangadir/workspace/Local/$job_name

dirs=(`ls -1|egrep -v 'input|output'`)
for dir in $dirs; do
    cd $dir/output;
    tar xfz ../input/_input_sandbox_14_0.tgz ./input_files ./output_files
    cd -;
done
