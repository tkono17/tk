#!/usr/bin/env zsh

function usage() {
    echo "Usage: $0 <tex_base_name>"
}

project_name=""
texfile_name=""
if [[ ${#*} -ne 1 ]]; then
    usage
    exit 0
else
    project_name=$1;
    texfile_name=$1.tex;
fi

sed s/PROJECT=/PROJECT=${project_name}/ \
    ${TK_ROOT}/share/Makefile_tex.template > Makefile

if [[ -e $texfile_name ]]; then
    echo "$texfile_name already exists, keep it"
else
    echo "Creating empty file $texfile_name"
    touch $texfile_name
fi
