#!/usr/bin/env zsh
#-------------------------------------------------------------------------
# ganga_status.sh
#-------------------------------------------------------------------------

ganga  -o'[PollThread]autostart=True' $TK_ROOT/python/ganga_status.py
