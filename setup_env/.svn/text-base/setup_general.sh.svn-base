#--------------------------------------------------------------------------
# tk/setup_general.sh
#--------------------------------------------------------------------------

##### General settings
export tk_svnroot=svn+ssh://lxplus.cern.ch/afs/cern.ch/user/t/tkohno/scratch0/svnroot/repos
export qfcalc_svnroot=http://subversion.assembla.com/svn/qfcalc
if [[ $OCHA_SVN == "" ]]; then
    export OCHA_SVN=svn+ssh://hpxr1.phys.ocha.ac.jp/var/svn/repos
fi

export RSYNC_RSH=ssh
export CVS_RSH=ssh
export SVN_RSH=ssh

alias cdw="cd $workdir"
alias cdd="cd $datadir"

##### For convenience
alias ls='/bin/ls -CF'
alias root='root -l'
alias xterm='xterm -sb -sl 1000'
unset fignore
unset autologout
# set ignoreeof
which xset >& /dev/null
if [[ $? == 0 ]]; then
    # turn off beeping
    xset b off
else
    xset b off >& /dev/null
fi
if [[ $HOST == atdesy9 ]]; then
    xset m 5 10
fi

alias start_ssh_agent='eval $(ssh-agent)'
alias kill_ssh_agent='ssh-agent -k'

autolist=ambiguous
prompt="%m:%/> "
export _JAVA_OPTIONS="-Xms256m -Xmx1024m"
export EDITOR='emacs -nw'

