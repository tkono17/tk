#!/usr/bin/env zsh

function usage() {
    echo "Usage: $0";
}

if [[ $TestArea == "" ]]; then
    usage()
    exit 1;
fi

install_area=$TestArea/InstallArea

install_area_lib=$install_area/$CMTCONFIG/lib
install_area_bin=$install_area/$CMTCONFIG/lib
install_area_jobOptions=$install_area/jobOptions
install_area_python=$install_area/python

echo $install_area_lib
