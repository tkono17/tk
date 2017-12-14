#!/usr/local/bin/zsh
#------------------------------------------------------------------------
# ath_cd_project.sh <project_name>
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# Functions
function usage() {
    echo "Usage: $1 <project_name>"
    echo "------"
    echo "Example: $1 AtlasEvent"
    exit 1;
}
#------------------------------------------------------------------------

if [[ $# -eq 0 ]]; then
    usage $0;
fi
project_name=$1;


project_path=""

# a=(`cmt show path | grep /${project_name}/`)
a=(`echo $CMTPATH|sed "s/:/\\n/g" | grep "/${project_name}/"`)
if [[ $#a -eq 0 ]]; then
    echo "Error: Project name ${project_name} not found in CMT path"
    exit 1;
# elif [[ ${#a} -ge 4 ]]; then
elif [[ ${#a} -eq 1 ]]; then
    project_path=$a[1];
fi

if [[ $project_path != "" ]]; then
    echo $project_path;
else
    echo "Error: Project name ${project_name} diretory not found in CMT path"
    exit 1;    
fi

exit 0
