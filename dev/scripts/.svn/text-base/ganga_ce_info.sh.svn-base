#!/usr/bin/env zsh
#--------------------------------------------------------------------------
# Investigates the information of CEs
#--------------------------------------------------------------------------

function usage() {
    echo "Usage: $1 <CE>"
}

if [[ $# -ne 1 ]]; then
    usage $0;
    exit 1;
fi

ce_name=$1;

lcg-infosites --vo atlas ce > lcg_ce.out

egrep "$1|^#|^-" lcg_ce.out > ceinfo_$1.txt
a=(`wc -l ceinfo_$1.txt`)
# echo $a[1]
if [[ $a[1] -ge 3 ]]; then
    (( n = $a[1] - 2 ))
    b=(`grep $1 ceinfo_$1.txt`)
    for ((i=0; $i<$n; i+=1)); do
	((j1=$i*6 + 1))
	((j2=$i*6 + 2))
	((j3=$i*6 + 3))
	((j4=$i*6 + 4))
	((j5=$i*6 + 5))
	((j6=$i*6 + 6))
	n_cpu=$b[$j1]
	n_free=$b[$j2]
	n_total=$b[$j3]
	n_running=$b[$j4]
	n_waiting=$b[$j5]
	name=$b[$j6]
	echo "CE name: $name"
	echo "N (CPU)     : $n_cpu"
	echo "N (free)    : $n_free"
	echo "N (total)   : $n_total"
	echo "N (running) : $n_running"
	echo "N (waiting) : $n_waiting"
    done
fi

