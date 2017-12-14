#!/usr/bin/env zsh
#---------------------------------------------------------------------
# svnWorkTool.sh
# --------------
# This tool provides some features useful for working with SVN
#---------------------------------------------------------------------

shortopts="tlpudah"
longopts="lasttag,listtags,package-path,url,dump,atlas-svn,remove-trunk,help"
args=(`getopt -l $longopts $shortopts -- $*`)

svn_info_out=`svn info`
svn_root=`echo $svn_info_out | grep 'Repository Root: '|sed "s/.*: //"`
url=`echo $svn_info_out | grep 'URL: ' | sed "s/.*: //"`
tags_path=`echo $url | sed "s/trunk.*/tags/"`
package_path=$url[${#svn_root}+2,-1]

dump_package_path=no
dump_url=no
do_dump=no

while [[ $# -ge 1 ]]; do
    opt=$1
    OPTARG=$2
    case $opt in
	
	-t|--lasttag)
	    shift;;
	-l|--list-tags)
	    svn ls $tags_path
	    shift;;
	-p|--package-path)
	    dump_package_path=yes
	    shift;;
	-u|--url)
	    dump_url=yes
	    shift;;
	--remove-trunk)
	    package_path=`echo $package_path | sed "s/\/trunk//"`
	    url=`echo $url | sed "s/\/trunk//"`
	    shift;;
	-d|--dump)
	    do_dump=yes
	    shift;;
	-a|--atlas-svn)
	    shift;;
	-h|--help)
	    shift;;
    esac
done

if [[ $do_dump != no ]]; then
    echo "svn_root=$svn_root"
    echo "package_path=$package_path"
fi

if [[ $dump_url != no ]]; then
    echo $url
fi

if [[ $dump_package_path != no ]]; then
    echo $package_path
fi


