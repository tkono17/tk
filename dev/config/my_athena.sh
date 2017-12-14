#!/usr/bin/env zsh

function addCmtPackage() {
# $1 cmt package name (will use cmt macros $(1)_home and $(1)_linkopts)
# $2 A cmt directory to invoke cmt commands
    package=$1
    package_home=`cd $(2); cmt show macro_value ${package}_home`
    linkopts=`cd $(2); cmt show macro_value ${package}_linkopts`
    echo CXXFLAGS += -I${package_home}/include
    echo INCFLAGS += -I${package_home}/include
    echo LIBS     += $linkopts
}

function addCmtPackages() {
# $1 cmt_project_path
# $2 list of packages
    cmt_path=$1
    packages=($2)
    cxxflags=()
    incflags=()
    libs=-L$(1)/InstallArea/$(CMTCONFIG)/lib
    for p in $packages; do
	cxxflags=" $cxxflags -I${cmt_path}/InstallArea/include/$p"
	incflags=" $incflags -I${cmt_path}/InstallArea/include/$p"
	libs=$libs -l$p
    done
    CXXFLAGS += $cxxflags
    INCFLAGS += $incflags
    LIBS     += $libs
}


