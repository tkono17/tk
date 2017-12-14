#!/usr/bin/env zsh

function usage() {
    echo "Usage: $1 [options] [<dir>=`pwd`]"
    echo "------"
    echo "Options: -p <packagelist> ..... List of packages"
    echo "         -a <testarea> ........ TestArea [=.]"
    echo "         -b ................... do broadcast [default=no]"
    echo "         -c ................... do config [default=no]"
    echo "         -m ................... do make [default=yes]"
    echo "         -n ................... do clean [default=no]"
    echo "         -q ................... do checkreq"
    echo "         -r ................... do reset (remove $CMTCONFIG) [no]"
    echo "         -v ................... do versioncmt (create version.cmt if not there)"
    echo "         -o ................... SVN checkout"
    echo "         -u ................... SVN update"
    echo "         -s ................... SVN status"
    echo "         -i ................... SVN commit"
    echo "         --comment ............ comment"
    echo "         -h ................... help"
    echo "Examples: $1 -b -m -p packages.txt"
}

packagelist="packages.txt"
testarea=`pwd`
bropt=""
do_config=no
do_setup=no
do_make=yes
do_clean=no
do_reset=no
do_versioncmt=no
do_checkreq=no
do_svn_checkout=no
do_svn_commit=no
do_svn_update=no
do_svn_status=no

while getopts a:b:p:cqsmrvhoiu opt; do
    case $opt in
	"p")
	    packagelist=$OPTARG;;
	"a")
	    testarea=$OPTARG;;
	"b")
	    bropt=br;;
	"c")
	    do_config=yes;;
	"m")
	    do_make=yes;;
	"n")
	    do_clean=yes;;
	"q")
	    do_checkreq=yes;;
	"r")
	    do_reset=yes;;
	"v")
	    #do_make=no;
	    do_versioncmt=yes;;
	"o")
	    do_make=no
	    do_svn_checkout=yes;;
	"u")
	    do_make=no
	    do_svn_update=yes;;
	"s")
	    do_make=no
	    do_svn_status=yes;;
	"i")
	    do_make=no
	    do_svn_commit=yes;;
	"h")
	    usage $0;
	    exit 0;;
    esac
done


curdir=`pwd`
cd $testarea
if [[ -e $packagelist ]]; then
    packages=(`cat $packagelist | grep -v '#'`)
else;
    echo "Creating the list of packages in $packagelist (testarea=$testarea)"
    ath_ls_packages.sh . > $packagelist
    packages=(`cat $packagelist | grep -v '#'`)
fi

good_packages=()
bad_packages=()

if [[ $do_clean == "yes" || $do_reset == "yes" || \
    $do_svn_update == yes || $do_svn_commit == yes || \
    $do_svn_checkout == yes ]]; then
    do_config=no
    do_setup=no
    do_make=no
fi

if [[ $do_checkreq == "yes" ]]; then
    do_make=no
fi

# echo "packages: $packages"
for pack in $packages; do
    echo "Working on package: $pack"
    ok=0
    if [[ $do_svn_checkout == "yes" ]]; then
	mkdir -p $testarea/$pack;
	svn co $SVNUSR/tkohno/$pack/trunk $pack
	#svn update
	cd $testarea/$pack/cmt
	pname=`basename $pack`
	echo "create version.cmt"
	echo "${pname}-99-99-99" > version.cmt
	cd -
    fi
    cd $testarea/$pack/cmt
    if [[ $do_versioncmt == "yes" && ! -e version.cmt ]]; then
	pname=`basename $pack`
	echo "create version.cmt"
	echo "${pname}-99-99-99" > version.cmt
    fi
    if [[ $do_checkreq == "yes" ]]; then checkreq.py; fi
    if [[ $do_config == "yes" ]]; then cmt $bropt config; fi
    if [[ $do_setup == "yes" ]]; then source setup.sh; fi
    if [[ $do_make == "yes" ]]; then
	cmt $bropt make;
	ok=$?
    fi
    if [[ $do_clean == "yes" ]]; then cmt $bropt clean; fi
    if [[ $do_reset == "yes" ]]; then rm -fr ../$CMTCONFIG; fi
    if [[ $do_svn_update == "yes" ]]; then
	cd $testarea/$pack/;
	svn update
	cd -
    fi
    if [[ $do_svn_status == "yes" ]]; then
	cd $testarea/$pack/;
	svn status -u
	cd -
    fi
    if [[ $do_svn_commit == "yes" ]]; then
	cd $testarea/$pack/;
	svn ci -m "Commit to SVN"
	cd -
    fi
    if [[ $ok != 0 ]]; then
	bad_packages=($bad_packages $pack)
    else;
	good_packages=($good_packages $pack)
    fi
    cd $testarea
done

cd $curdir

echo "Build succeeded for packages: "
for p in $good_packages; do
    echo "  $p"
done
echo "Build failed for packages: "
for p in $bad_packages; do
    echo "  $p"
done


