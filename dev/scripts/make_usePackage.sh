#!/usr/bin/env zsh
#-----------------------------------------------------------------------
# A tools to generate configurations for make
#-----------------------------------------------------------------------

cxxflags=
incflags=
libs=

function find_package() {
    package=$1
    dir=$2

    if [[ -e ${dir}/include/$package && \
	-e ${dir}/lib/lib${package}.so ]]; then
	cxxflags="-I${dir}/include/${package}"
	incflags="-I${dir}/include/${package}"
	libs="-L${dir}/lib -l${package}"
	echo "# Configuration taken from installed area ${dir}"
	echo "CXXFLAGS = $cxxflags"
	echo "INCFLAGS = $incflags"
	echo "LIBS     = $libs"
    fi
}

function check_dir() {
    package=$1
    dir=$2

    fragment=${dir}/${package}.makefile

    if [[ -e ${fragment} ]]; then
	echo "# Configuration taken from ${fragment}"
	cat ${fragment}
    else
	find_package $package $dir
    fi
}

function use_package() {
    package=$1
    dirs=(${ProjectDir} ${TK_INSTALL_DIR} ${TKDEV_ROOT}/config)

    for dir in $dirs; do
	check_dir $package $dir
    done
}

if [[ $# -ge 1 ]]; then
    arg1=$1
    if [[ ${arg1[1]} == "-" ]]; then
	echo "Usage $0 <package>"
    else
	use_package $1
    fi
fi
