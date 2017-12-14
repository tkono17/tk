#!/bin/bash

release=12.0.6
jobOptions="HelloWorldOptions.py"

source $VO_ATLAS_SW_DIR/software/$release/setup.sh
source $SITEROOT/AtlasOffline/$release/AtlasOfflineRunTime/cmt/setup.sh

alias dq2_ls='noglob dq2_ls'
dq2_ls -g *005105.PythiaWmunu.recon.AOD*

# athena.py $jobOptions

