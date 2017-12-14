#!/usr/bin/env zsh
# set script_dir='/raid3/kohno/mvd/programs/scripts'
# set config_dir='/raid3/kohno/programs/config'
set config_dir=${TKDEV_ROOT}/config
# set dirs='inc src obj lib exe doc'
set dirs='src obj lib exe doc'
if($#argv == 1) then
    set proj_dir=$argv[1]
    echo "project directory is ${proj_dir}"
    mkdir ${proj_dir}
    cd ${proj_dir}
else
    set temp=`pwd`
    set proj_dir=${temp:t}
endif
mkdir ${dirs} ${proj_dir}
cp ${config_dir}/Makefile .
cp ${config_dir}/my.makefile .
cp ${config_dir}/mydep.makefile .
