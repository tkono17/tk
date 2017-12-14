#!/usr/bin/env zsh
#-----------------------------------------------------------------------
#
#-----------------------------------------------------------------------

function usage() {
  echo "Usage: $0 <project_name>"
  echo "  This command will create a new directory with the same name"
  echo "  as the project name with the standard directory structure and "
  echo "  a CMakeLists.txt file."
}


if [[ $# == 1 ]]; then
    usage()
    exit 1
fi

pname=$1 # project name

mkdir ${pname}
if [[ $? == 0 ]]; then
    echo "Created a new directory '${pname}'"
    cd $pname
    mkdir $pname src
    f_hin=${pname}/${pname}Config.h.in
    cat $TKDEV_ROOT/scripts/cmakelists_template.txt | \
	sed "s/__PROJECT_NAME__/${pname}/g" > CMakeLists.txt
    echo "#define ${pname}_VERSION_MAJOR @${pname}_VERSION_MAJOR@">> ${f_hin}
    echo "#define ${pname}_VERSION_MINOR @${pname}_VERSION_MINOR@">> ${f_hin}
    cd -
fi

