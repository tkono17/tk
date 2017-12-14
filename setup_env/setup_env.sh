#--------------------------------------------------------------------------
# tk/setup_env.sh
#----------------
# Add the following line to .zshrc (path must be modified appropriately)
# source $HOME/work/tk/setup_env/setup_env.sh
#--------------------------------------------------------------------------
#echo "Setup my environment"

self=$0
dir=$HOME
if [[ ${#self} -gt 0 && ${self[1]} != "/" ]]; then
    dn=$(dirname $self)
    bn=$(basename $self)
    self=$(cd $dn; pwd)/$(basename $self)
fi
dir=$(dirname $self)
host=$(hostname -s)
domain=$(hostname -d) >& /dev/null

#echo "Applying local setup for $host/$domain"
if [[ $domain == "desy.de" ]]; then
    source ${dir}/local_desy.sh
    if [[ $host != "bastion" ]]; then
	sync=yes
    fi
elif [[ $domain == "naf.desy.de" ]]; then
    source ${dir}/local_naf.sh
    sync=yes
elif [[ $domain == "cern.ch" ]]; then
    source ${dir}/local_cern.sh
    sync=yes
elif [[ $domain == "icepp.jp" ]]; then
    source ${dir}/local_icepp.sh
    sync=yes
elif [[ ${host[1,6]} == hpxpc5 ]]; then
    source ${dir}/local_ocha2.sh
    sync=yes
elif [[ $domain == "ocha.ac.jp" || ${host[1,3]} == hpx ]]; then
    source ${dir}/local_ocha.sh
    sync=yes
#elif [[ $domain == "" && $host == "TK-Vaio-VirtualBox" ]]; then
elif [[ $domain == "" && $host == "tkohno-VirtualBox" ]]; then
    source ${dir}/local_laptop.sh
    sync=yes
else
    echo "Domain $domain not registered, not applying any local setting"
fi

source ${dir}/setup_general.sh
source ${dir}/setup_work.sh

tty >& /dev/null
if [[ $? == 0 && $sync == "yes" ]]; then
#    mycron.py start
fi

