#!/usr/bin/env zsh

cat <<EOF
1. Release setup

asetup AnalysisBase,21.2.93

21.0: Tier-0 release
21.1: HLT at Point1
21.2: Analysis and derivation
21.3: Simulation development
21.6: Event generation

2. On every login

cd ../build
asetup --restore
source x86_64-*/setup.sh

EOF
