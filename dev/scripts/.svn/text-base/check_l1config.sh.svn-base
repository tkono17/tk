#!/usr/bin/env zsh

function usage() {
    echo "Usage: check_l1config.sh <L1config.xml>"
}

if [[ $# -ne 1 ]]; then
    usage
    exit 1
fi

fname=$1;

echo "Total number of LVL1 thresholds: " `grep "<TriggerThreshold\>" $fname |wc -l` "(/54)"
echo "  Number of MUON thresholds: " `grep "<TriggerThreshold\>" $fname |grep MUON|wc -l`
echo "  Number of EM thresholds  : " `grep "<TriggerThreshold\>" $fname |grep "EM"|wc -l`
echo "  Number of TAU thresholds : " `grep "<TriggerThreshold\>" $fname |grep TAU|wc -l`
echo "  Number of JET thresholds : " `grep "<TriggerThreshold\>" $fname |grep JET|wc -l`
echo "  Number of JF thresholds  : " `grep "<TriggerThreshold\>" $fname |grep JF|wc -l`
echo "  Number of JB thresholds  : " `grep "<TriggerThreshold\>" $fname |grep JB|wc -l`
echo "  Number of JE thresholds  : " `grep "<TriggerThreshold\>" $fname |grep 'JE\"'|wc -l`
echo "  Number of TE thresholds  : " `grep "<TriggerThreshold\>" $fname |grep TE|wc -l`
echo "  Number of XE thresholds  : " `grep "<TriggerThreshold\>" $fname |grep XE|wc -l`
echo "Number of items: " `grep "<TriggerItem\>" $fname |wc -l`
