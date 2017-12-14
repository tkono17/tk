#!/usr/bin/env zsh
#--------------------------------------------------------------------------
function help() {
    cat <<EOF
Usage: $1 [<command> [<comment>]]
<command> : Make target (all|install|cleanall|...)
            SVN command (update|status|commit)
<comment> : Comment for SVN commit
EOF
}
#--------------------------------------------------------------------------

packages=()
config_file=packages.txt

if [[ $# -ge 1 && ($1 == "-h" || $1 == "--help")  ]]; then
    help $0
    exit 0
fi
echo "target=$1"
if [[ -e $config_file ]]; then
    packages=(`cat $config_file |grep -v '^#'`)
    echo "Reading packages from file $config_file ($#packages packages)"
fi

target=all
comment='commit'
if [[ $# -ge 1 ]]; then
    target=$1
fi
if [[ $# -ge 2 ]]; then
    comment=$2;
fi

echo "Make target=$target"

if [[ ${#packages} -eq 0 ]]; then
    echo "No packages specified."
    echo "  ==> Please provide the list of packages in $config_file"
    exit -1;
fi

curdir=`pwd`
packages1=()
packages2=()
for p in $packages; do
    echo "Building $p (target=${target}) ..."
    cd $p;
    if [[ $target == any ]]; then
	#svn add cmd/Makefile #-m "Moving Makefile under cmd/"
	echo "Not doing anything"
    elif [[ $target == update ]]; then
	svn $target
    elif [[ $target == status ]]; then
	svn $target -u
    elif [[ $target == commit ]]; then
	svn ci -m $comment
    else
	ss=0
	if [[ -e Makefile ]]; then
	    make $target
	    ss=$?
	elif [[ -e cmd/Makefile ]]; then
	    make -f cmd/Makefile $target
	    ss=$?
	else
	    echo "Makefile not found"
	fi
	if [[ $ss == 0 ]]; then
	    packages1=($packages1 $p)
	else
	    packages2=($packages2 $p)
	fi
    fi
    cd $curdir
done

echo "*** Successfully processed packages ($target)"
for p in $packages1; do
    echo "$p"
done
echo ""
echo "*** Failed packages ($target)"
for p in $packages2; do
    echo "$p"
done
echo ""

