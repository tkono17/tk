#!/usr/local/bin/zsh
#------------------------------------------------------------------------
# ath_runcmt.sh <requirements>
#------------------------------------------------------------------------

req_file=$1;

#------------------------------------------------------------------------
# Functions
function usage {
    echo "Usage: ath_runcmt.sh <requirements>"
}

#------------------------------------------------------------------------

if [[ ! -e $req_file ]]; then
    echo "Error: Requirements file: $req_file does not exist"
    usage
    exit 1
fi

#------------------------------------------------
# Transform a line like 
# use <package> <package-version> <path>
# into
# <path>/<package>
#------------------------------------------------
packs=(`grep '^use' $req_file |
    sed 's/^use[[:space:]]\+\([[:alnum:]]\+\)[[:space:]]\+[[:alpha:]][[:alnum:]-]\+[[:space:]]\+\([[:alnum:]\/]\+\)/\2\/\1/'`)

versions=(`grep '^use' $req_file |
    sed 's/^use[[:space:]]\+\([[:alnum:]]\+\)[[:space:]]\+([[:alpha:]][[:alnum:]-]\+)[[:space:]]\+\([[:alnum:]\/]\+\)/\2/'`)

(( i=0 ))
echo "$#packs packages to compile"
for p in $packs; do
    echo "Compiling $p"
    #echo "cmt co -r $versions[$i] $p"
    #(( i = $i + 1))
    #continue
    cd $p/cmt
    cmt config
    source setup.sh
    cmt br make
    cd -
done

