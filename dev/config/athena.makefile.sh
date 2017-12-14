#!/usr/bin/env zsh

function addCmtPackage() {
# $1 cmt package name (will use cmt macros $(1)_home and $(1)_linkopts)
# $2 A cmt directory to invoke cmt commands
    package=$1
    package_home=`cd $2; cmt show macro_value ${package}_home`
    linkopts=`cd $2; cmt show macro_value ${package}_linkopts`
    echo CXXFLAGS += -I${package_home}/include
    echo INCFLAGS += -I${package_home}/include
    echo LIBS     += $linkopts
}

function addCmtPackages() {
# $1 cmt_project_path
# $2 list of packages
    cmt_path=$1
    packages=(${@[2,-1]})
    cxxflags=()
    incflags=()
    libs=-L${cmt_path}/InstallArea/${CMTCONFIG}/lib
    for p in $packages; do
	cxxflags=" $cxxflags -I${cmt_path}/InstallArea/include/$p"
	incflags=" $incflags -I${cmt_path}/InstallArea/include/$p"
	libs="$libs -l$p"
    done
    echo CXXFLAGS += $cxxflags
    echo INCFLAGS += $incflags
    echo LIBS     += $libs
}

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 -p <package> <cmt_dir>"
    echo "       $0 -s <project_area> <package_list>"
    echo "-------"
    echo "Examples: $0 -p CLHEP khep/KHepBase/cmt"
    echo "          $0 -s \$TestArea KHepBase KHepUtil"
elif [[ $1 == "-p" ]]; then
    addCmtPackage $2 $3
elif [[ $1 == "-s" ]]; then
    addCmtPackages $2 ${@[3,-1]}
fi

