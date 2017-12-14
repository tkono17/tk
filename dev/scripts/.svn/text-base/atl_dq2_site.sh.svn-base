#!/usr/bin/env zsh

resubmit_jobs=(
    run00154810
    run00155697
    run00158548
    run00158582
    run00158632
    run00159113
    run00162843
    run00162882
    run00165591
    run00165956
    run00166143
    run00166856
    run00166964
    run00167576
    run00167607
    run00167680
    run00167776
)

favorite_sites=(
    DESY-HH
    DESY-ZN
)

grl_dir=$workdir/work/GRL/WZjets

runlists1=(
    wzjets_2010.periodA
    wzjets_2010.periodB
    wzjets_2010.periodC
    wzjets_2010.periodD
    wzjets_2010.periodE
    wzjets_2010.periodF
    wzjets_2010.periodG
    wzjets_2010.periodH
    wzjets_2010.periodI
)

for x in $resubmit_jobs; do
    echo $x
    for y in $runlists1; do
	dsfile=${grl_dir}/${y}_AOD.sh
	a=`grep $x $dsfile`
	if [[ $a != "" ]]; then
	    source $dsfile
	    ds=$datasets[$x]
	    echo "Job $x belongs to runlist $y => $ds"
	    dq2-ls -f $ds | grep -A 100 ' COMPLETE' | grep DESY-HH
	    break
	fi
    done
done
