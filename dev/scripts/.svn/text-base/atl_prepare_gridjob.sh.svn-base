#!/usr/bin/env zsh
#-------------------------------------------------------------------
# Prepare grid jobs given input DS
#-------------------------------------------------------------------

name='job'
grlds_fname=''
output_fname='gridjob_submit.sh'
jo=
n=1
output_files=()
workdir=.

function usage() {
    echo "Usage: $1 [options]"
    echo "------
-f <input_file> .... Input file which is the output from atl_grl_ds.py
-o <output_file> ... Output file with commands to submit jobs
-j <joboptions> .... Job options file
-n <n> ............. Number of files per job
-h ................. Help"
}

function getDS() {
    tag=$1;
    hookfile=$2;
    if [[ -e tmpfile.txt ]]; then rm tmpfile.txt; fi
    echo "$tag" > tmpfile.txt
    insert_in_tag.py -t '^#TAG' tmpfile.txt tmpfile2.txt $hookfile
    inDS=`grep inDS tmpfile2.txt`
    outDS=`grep outDS tmpfile2.txt`
    rm -fr tmpfile.txt tmpfile2.txt
    echo "$inDS $outDS"
}

#-------------------------------------------------------------
# Decode arguments
#-------------------------------------------------------------
cmd=$0;
args=(`getopt 'f:j:n:o:h' $*`)

while [[ $# -ge 1 ]]; do
    opt=$1;
    OPTARG=$2;
    #echo "opt=$opt"
    case $opt in 
	"-f")
	    grlds_fname=$OPTARG
	    shift 2;;
	"-o")
	    output_fname=$OPTARG
	    shift 2;;
	"-j")
	    jo=$OPTARG
	    shift 2;;
	"-n")
	    n=$OPTARG
	    shift 2;;
	"-h")
	    usage $cmd;
	    exit 0
	    shift;;
    esac
done

#-------------------------------------------------------------
# Check settings
#-------------------------------------------------------------
stopit=no
if [[ ! -e $grlds_fname ]]; then
    print 'Warning: input file with datasets does not exist'
    stopit=yes
fi
if [[ $jo == '' || ! -e $jo ]]; then
    print "Warning: JobOptions file '$jo' does not exist"
    stopit=yes
fi
if [[ $stopit == "yes" ]]; then
    echo ""
    usage $cmd
    exit -3
fi

#-------------------------------------------------------------
# Main part
#-------------------------------------------------------------
tags=(`grep '#TAG-' $grlds_fname | grep _begin | sed "s/_begin//g"`)

jnamelist=()
inDSlist=()
outDSlist=()

for tag in $tags; do
    inDS=
    outDS=
    echo $tag
    ds=(`getDS $tag $grlds_fname`)
    #echo $ds
    #echo "$ds[1]"
    #echo "$ds[2]"
    jnamelist=($jnamelist `echo $ds[1] | sed "s/inDS=//"`)
    inDSlist=($inDSlist $ds[1])
    outDSlist=($outDSlist $ds[2])
done

nds=${#inDSlist}
echo "N datasets: $nds"

if [[ -e $output_fname ]]; then
    rm $output_fname
fi

echo "#!/usr/bin/env zsh" >> $output_fname
echo "#---------" >> $output_fname
echo "" >> $output_fname
echo "function submit() {
    job_name=\$1
    inDS=
    outDS=
    jo=
    n=
    case \$job_name in " >> $output_fname

i=1
while [[ $i -le $nds ]]; do
#if [[ $inDS != "" && $outDS != "" && -e $jo ]]; then
    inDS=$inDSlist[$i]
    outDS=$outDSlist[$i]
    job_name=$inDS
    echo "        '$job_name')" >> $output_fname
    echo "            inDS=$inDS" >> $output_fname
    echo "            outDS=$outDS" >> $output_fname
    echo "            jo=$jo" >> $output_fname
    echo "            n=$n;;" >> $output_fname
    #echo "    "panda_submit.sh -i $inDS \
#	-o $outDS \
#	-j $jo \
#	-n $n";;" >> $output_fname
    #echo "" >> $output_fname
    (( i = $i + 1 ))
done
echo "    esac" >> $output_fname
echo '    panda_submit.sh -i $inDS -o $outDS -j $jo -n $n' >> $output_fname
echo "}\n\n" >> $output_fname

echo "jobs=(
    `echo $jnamelist | sed 's/ /\n    /g'`
)" >> $output_fname
echo 'for j in $jobs; do' >> $output_fname
echo '    submit $j' >> $output_fname
echo "done" >> $output_fname

if [[ -e $output_fname ]]; then
    echo "Grid job submission commands written to file '$output_fname'"
    chmod +x $output_fname
fi

