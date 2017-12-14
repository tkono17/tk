#!/usr/local/bin/zsh

#---------------------------------------------------------------
# Parameters
tkathena_external=$TestArea/TkAthena/External
lib_from_tkdev=(\
    KHepBase\
    KHepRoot\
    )
#---------------------------------------------------------------

if [[ $TK_ROOT == "" ]]; then
    echo "TK_ROOT environment is not set"
    exit 0
fi
if [[ $TestArea == "" ]]; then
    echo "ATHENA TestArea environment is not set"
    exit 0
fi


for a in $lib_from_tkdev; do
    src=${TKDEV_ROOT}/khep/$a;
    (cd $src; make cleanbak >& /dev/null)
    dest_dir=$tkathena_external/$a;
    if [[ ! -e $dest_dir ]]; then
	(cd $TestArea; cmt create $dest_dir $a-00-00-00)
    fi
    if [[ -e $src ]]; then
	# Copy header files
	files=(`ls ${src}/$a/*.hxx`)
	if [[ ! -e $dest_dir/$a; ]]; then
	    echo "Making directory $dest/$a";
	    mkdir -p $dest_dir/$a;
	fi
	for f in $files; do
	    dest=$dest_dir/$a/`basename $f`
	    if [[ ! -e $dest || $dest -ot $f ]]; then
		echo "Linking file $f ..."
		rm $dest;
		cp $f $dest;
		# (cd $dest; ln -s $f .)
	    fi
	done
	# Copy source files
	files=(`ls ${src}/src/*.cxx`)
	if [[ ! -e $dest_dir/src; ]]; then
	    echo "Making directory $dest/src";
	    mkdir -p $dest_dir/src;
	fi
	for f in $files; do
	    dest=$dest_dir/src/`basename $f`
	    fbase=`basename $f`
	    tmp=`echo $fbase| grep -v Dict`
	    echo "fbase = $fbase"
	    echo "tmp = $tmp"
	    if [[ $tmp != $fbase ]]; then
		continue
	    fi
	    if [[ ! -e $dest || $dest -ot $f ]]; then
		echo "Linking file $f ..."
		# ln -s $f $dest;
		rm $dest;
		cp $f $dest;
		# (cd $dest; ln -s $f .)
	    fi
	done
    else
	echo "$src does not exist"
    fi
done
