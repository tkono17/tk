#!/usr/bin/env zsh
#-----------------------------------------------------------
#
#-----------------------------------------------------------

#-------------------------------------
# Parameters taken from options
#-------------------------------------
show_help=no

#-------------------------------------
# Internal data
#-------------------------------------
config_dir=${TKDEV_ROOT}/config
dirs=(src obj lib exe doc)

#-------------------------------------
# Read arguments
#-------------------------------------
if [[ ${#argv} == 1 ]]; then
    proj_dir=$argv[1]
    if [[ $proj_dir == -h || $proj_dir == --help ]]; then
	show_help=yes
    else
	echo "project directory is ${proj_dir}"
	mkdir ${proj_dir}
	cd ${proj_dir}
    fi
else
    temp=`pwd`
    proj_dir=${temp:t}
fi

#-------------------------------------
# Main program
#-------------------------------------
if [[ $show_help == yes ]]; then
    echo "make_dir.sh [<project_name>] # Default <project_name>=."
fi

for d in $dirs; do
    if [[ ! -d $d ]]; then
	mkdir $d 
    fi
done
if [[ ! -d $proj_dir ]]; then
    mkdir $proj_dir
fi

if [[ ! -e Makefile ]]; then
    cat ${config_dir}/Makefile | sed "s/<REPLACE_WITH_PACKAGE_NAME>/${proj_dir}/" > ./Makefile
fi
if [[ ! -e my.makefile ]]; then
    cp ${config_dir}/my.makefile .
fi
if [[ ! -e mydep.makefile ]]; then
    cat ${config_dir}/mydep.makefile | sed "s/<REPLACE_WITH_PACKAGE_NAME>/${proj_dir}/" > ./mydep.makefile
fi

