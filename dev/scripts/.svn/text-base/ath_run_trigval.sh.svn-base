#!/usr/bin/env zsh

n=$1
if [ -z "$n" ]; then
  n=1
fi

mkdir -p run$n
cd run$n

conf_file=$AtlasArea/../../AtlasTrigger/$AtlasVersion/Trigger/TrigValidation/TriggerTest/Testing/trigValidation.conf 

tests=(
    AthenaModernRDO
    AthenaXMLConfigRDO 
    AthenaModernRDO_lumi0.01_no_Bphysics_no_prescale 
    AthenaModernBS_standalone 
    standalone_cosmic
)

for tt in $tests; do
    echo "Running $tt ..."
    trigtest.pl --test $tt \
	--rundir $tt \
	--config $conf_file \
	> i${tt}.log 2>&1
done

