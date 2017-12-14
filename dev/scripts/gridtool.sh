#!/usr/local/bin/zsh

castor_status=""

check_castor() {
    a=`ls $1`
    is_there="no"
    if [[ $a == "" ]]; then
	is_there="no"
    else
	is_there="yes"
    fi
    echo "result for $1 : $is_there\n"
    castor_status=$is_there
}

a=`check_castor $1`
echo "a=$castor_status";
echo "hello"
