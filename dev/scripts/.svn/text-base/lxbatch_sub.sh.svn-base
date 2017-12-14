#!/usr/bin/env zsh

joblist='joblist'
script_name='script.sh'
queue=1nh

function usage() {
    echo "Usage: $1 <joblist> <script_name> <queue>"
}

if [[ $# -lt 3 ]]; then
    usage $0
    exit 1
fi

if [[ $# -ge 1 ]]; then
    joblist=$1;
fi
if [[ $# -ge 2 ]]; then
    script_name=$2;
fi
if [[ $# -ge 3 ]]; then
    queue=$3
fi

jobs=(`cat $joblist`)
for job in $jobs; do
    cd $job;
    echo "Submitting job $job to queue $queue"
    bsub -q $queue $script_name;
    cd ..
done



