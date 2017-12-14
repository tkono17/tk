#!/usr/bin/env zsh
#--------------------------------------------------------------------------
function help() {
}
#--------------------------------------------------------------------------
# (only accept jobs with correct resources)
#$ -w e
#_run_type=loca
# (stderr and stdout are merged together to stdout)
#$ -j y
#
# (put log files into current working directory)
#$ -cwd
#
# # (use ATLAS project)
# ### -$ -P atlas
# (2-days queue)
#$ -l h_rt=6:00:00
# #$ -l h_rt=47:59:00
#### example: qsub -t ${i}-${i} -l h_vmem=2048M -l h_fsize=12G  -l h_rt=47:59:00 runFittinoSGE.sh -i ... -o ...

#--------------------------------------------------------------------------
# 1. Set environment variables
# 2. Setup before running the main job
# 3. Run job
# 4. Copy output files
#--------------------------------------------------------------------------
ProjectDir=cfg_projectdir
name='test'
job_class=${job_class}
config_file=${config_file}
input_file_list=${input_file}
output_file=$output_file
logfile=${logfile}
workdir=${workdir}

naf=$do_naf
if [[ $SGE_O_HOME != "" ]]; then
    naf=yes
else
    naf=no
fi
#TAG-SETUP-ENV

curdir=\`pwd\`
ini ROOT527
source ${ProjectDir}/scripts/runtime_setup.sh

if [[ $naf == yes ]]; then
    echo 'Dump environment'
    printenv
    echo 'Dumped environment'
    cd $TMP
fi

if [[ -e $logfile ]]; then
    rm $logfile
fi
if [[ -e $output_file ]]; then
    rm $output_file
fi
runTreeJob.exe \
    --run-dir $rundir \
    --input-file-list $input_file_list \
    --output-file $output_file \
    $job_class $config_file \
    >& $logfile

localdir=`pwd`
if [[ $localdir != $gTmpDir ]]; then
    echo "Copying files to output destination $gTmpDir"
    echo "Directory listing of $localdir"
    ls -l
    files=(\`ls *.log *.root\`)
    if [[ $? == 0 ]]; then
        for f in $file; do
            if [[ -e $f ]]; then
                cp $f $gTmpDir
            fi
        done
    fi
fi
