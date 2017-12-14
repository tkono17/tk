#!/usr/bin/env zsh

xsl_file=$TKDEV_ROOT/config/tksite.xsl

function convert() {
    f_input=$1
    f_output=$2
    sitetop=$3
    outdir=`dirname $f_output`
    if [[ ! -d $outdir ]]; then
	mkdir -p $outdir;
    fi
    if [[ ${#f_input} -ge 5 && ${f_input[-4,-1]} == ".php" \
	&& $python_exe != "" ]]; then
	# .php file (overwrite the $python_exe variable)
	f_input2=${f_input}.tmp
	cat $f_input | sed -e "/\$python_exe\s\+=/ c \
	    \$python_exe = '$python_exe';" > \
	    $f_input2
    else
	f_input2=$f_input
    fi
    cmd=(xsltproc --html --stringparam site-top "$sitetop")
    cmd=($cmd -o $f_output $xsl_file $f_input2)
    $cmd
    if [[ $f_input2 != $f_input && -e $f_input2 ]]; then
	rm $f_input2
    fi
}

function convertHtmlFiles() {
    localtop=`pwd`/local
    files=(`(cd src; find . -name '*.html|*.php')`)
    for f in $files; do
	if [[ $f[1,2] == "./" ]]; then
	    f=$f[3,-1]
	fi
	echo "Converting $f ..."
	convert src/$f local/$f $localtop
	convert src/$f site/$f ''
    done
}

function copyFile() {
    src=$1
    dest=$2

    destdir=`dirname $dest`
    if [[ -d $src ]]; then
	destdir=$dest
	if [[ ! -d $destdir ]]; then
	    echo "Create directory $destdir"
	    mkdir -p $destdir;
	fi
    else
	if [[ ! -d $destdir ]]; then
	    echo "Create directory $destdir"
	    mkdir -p $destdir;
	fi
	if [[ -L $dest ]]; then
	else
	    if [[ -e $dest ]]; then
		rm -f $dest;
	    fi
	    echo "Create symbolic link $dest"
	    ln -s `pwd`/src/$f $dest
	fi
    fi
}

function allFiles() {
    files1=(`(cd src; ls -1R | egrep -v '~$|\.html$|\.php$')`)
    files=()
    dir=.
    for f in $files1; do
	if [[ $f[-1] == ':' ]]; then
	    dir=$f[1,-2]
	else
	    fpath=${dir}/$f
	    fpath=`echo $fpath | sed "s/\.\///"`
	    if [[ ! -d src/$fpath ]]; then
		# Do not include directories
		files=($files $fpath)
	    fi
	fi
    done
    echo $files
}

function copyAllFiles() {
    files=(`allFiles`)
    for f in $files; do
	if [[ $f[1,2] == "./" ]]; then
	    f=$f[3,-1]
	fi
	# echo "Copying file $f ..."
	copyFile src/$f local/$f
	copyFile src/$f site/$f
    done
}

function createMakefile() {
    localtop=`pwd`/local
    if [[ -e Makefile ]]; then
	rm Makefile
    fi
    touch Makefile
    echo "default: all\n" >> Makefile
    echo "XSLfile := $xsl_file" >> Makefile
    echo "SITE_TOP := $sitetop" >> Makefile
    echo "SITE_DIR := $sitedir" >> Makefile

    # Web files (.html, .php)
    web_files=(`(cd src; find . -name '*.html')`)
    web_files=($web_files `(cd src; find . -name '*.php')`)
    web_files2=()
    for f in $web_files; do
	if [[ ${f[1,2]} == "./" ]]; then
	    f=$f[3,-1]
	fi
	web_files2=($web_files2 $f)
	src=src/$f
	echo "
local/$f: $src \$(XSLfile)\n\tmk_tkweb.sh -i \$< -o \$@ -l
site/$f: $src \$(XSLfile)\n\tmk_tkweb.sh -i \$< -o \$@" >> Makefile
    done
    web_files=($web_files2)
    echo "" >> Makefile
    for f in $web_files; do
	echo "LOCAL_HTMLS += local/$f" >> Makefile
    done
    echo "" >> Makefile
    for f in $web_files; do
	echo "SITE_HTMLS += site/$f" >> Makefile
    done

    # Other files
    misc_files=(`allFiles`)
    for f in $misc_files; do
	echo "" >> Makefile
	echo "local/$f: src/$f
\t@mkdir -p `dirname local/$f`
\t@if [[ ! -L \$@ ]]; then ln -s \$< \$@; fi" >> Makefile
	echo "site/$f: src/$f
\t@mkdir -p `dirname site/$f`
\t@if [[ ! -L \$@ ]]; then ln -s \$< \$@; fi" >> Makefile
    done
    for f in $misc_files; do
	echo "LOCAL_MISC_FILES += local/$f" >> Makefile
    done
    for f in $misc_files; do
	echo "SITE_MISC_FILES += site/$f" >> Makefile
    done

    #
    echo "\n" >> Makefile
    echo ".PHONY: all browse publish help" >> Makefile
    echo "all: \$(SITE_HTMLS) \$(LOCAL_HTMLS) \$(LOCAL_MISC_FILES) \$(SITE_MISC_FILES)\n" >> Makefile
    echo "site_htmls:
\t@echo \$(SITE_HTMLS)" >> Makefile

    echo "\n" >> Makefile
    echo "browse: 
\tfirefox local/index.html&
publish: \$(SITE_HTMLS) \$(SITE_MISC_FILES)
\t@echo 'Not yet publishing it'
\trsync -avzL site/* ${sitedir}
help:
\t@echo 'Targets: all: convert all html'
\t@echo '         browse: Browse the local site with a browser'
\t@echo '         publish: Publish the site to the web server'
\t@echo '         help:    Show this message'
" >> Makefile
}

cmd=`basename $0`
function usage() {
    echo "Usage: $cmd [options]
--------
Options:
--------
-a|--all-files
   copy all files except for *.html and *.php to local/ and site/
-i|--input-html <input_html>
   convert the input *.html file
-l|--local-site (default=no)
   convert html to the local (local/), otherwise to site/
-o|--output-html <output_html>
   output html file name
-m|--makefile
   create Makefile to do the job
-d|--delete-copy
   delete directories local/ and site/
-w|--web-files
   convert all *.html and *.php files under src/
-u|--update
   update the web server by copying everything under site/
-s|--site-top
   Site top URL (e.g. http://www.xxx.yy/topdir)
--site-dir
   Site top directory on the web server (e.g. user@host:dir)
--python-exe=<path_to_python_exe>
  Set path to the python executable on the web server
-b|--browse
   browse local files with web browser
-h|--help
   help
---------
Examples:
---------
$cmd -m
then
make all
make help

$cmd -a -w -m
$cmd -i input.html -o output.html -l # for local copy
$cmd -i input.html -o output.html # for web server"
}

do_all_files=no
do_html_files=no
do_update=no
browser=''
do_help=no
do_delete_copy=no
do_one_file=no
input_html=
output_html=
local_site=no
create_makefile=no
sitetop=http://cern.ch/tkohno/new
sitedir=tkohno@lxplus.cern.ch:www/WWW/new
python_exe=/afs/cern.ch/sw/lcg/external/Python/2.5.4p2/i686-slc5-gcc43-opt/bin/python

if [[ $# -eq 0 ]]; then
    do_all_files=yes
    do_html_files=yes
    do_update=no
    browser='' # `pwd`/local/index.html
    do_help=no
fi

# getopt 'lsub:h' -l 'local,site,update,browse=,help' $*;
#getopt 'lsub:h' $*;
while [[ $# -ge 1 ]]; do
    opt=$1
    OPTARG=$2
    case $opt in
	-a | --all-files)
	    do_all_files=yes
	    shift 1;;
	-i | --input-html)
	    do_one_file=yes
	    input_html=$OPTARG;
	    shift 2;;
	-l | --local-site)
	    local_site=yes
	    shift 1;;
	-o | --output-html)
	    output_html=$OPTARG;
	    shift 2;;
	-m | --makefile)
	    create_makefile=yes
	    shift 1;;
	-d | --delete-copy)
	    do_delete_copy=yes
	    shift 1;;
	-w | --html-files)
	    do_html_files=yes
	    shift 1;;
	-s | --site-top)
	    sitetop=$OPTARG;
	    shift 2;;
	--site-dir)
	    sitedir=$OPTARG;
	    shift 2;;
	--python-exe)
	    python_exe=$OPTARG;
	    shift 2;;
	-u | --update)
	    do_update=yes
	    shift 1;;
	-b | --browse)
	    browse=$OPTARG;
	    shift 2;;
	-h | --help)
	    do_help=yes
	    shift 1;;
    esac
done


if [[ $do_help != "no" ]]; then
    usage
    exit 0;
fi
if [[ $do_delete_copy != "no" ]]; then
    rm -fr site/*
    rm -fr local/*
fi

if [[ $do_one_file != "no" ]]; then
    if [[ $output_html == "" ]]; then
	output_html=`basename $input_html`
    fi
    if [[ $local_site != "no" ]]; then
	sitetop=`pwd`/local
    fi
    convert $input_html $output_html $sitetop
else
    if [[ $do_all_files != "no" ]]; then
	copyAllFiles
    fi
    if [[ $do_html_files != "no" ]]; then
	convertHtmlFiles
    fi
fi

if [[ $create_makefile != "no" ]]; then
    createMakefile
fi

