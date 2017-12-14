#!/usr/local/bin/zsh

a=`ath_cd_project.sh $1`
b=`echo $a | grep $1`
if [[ $a == $b ]]; then
    cd $a;
fi
