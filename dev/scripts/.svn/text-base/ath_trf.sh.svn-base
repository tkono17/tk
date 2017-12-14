#!/usr/bin/env zsh

fprefix='ABC'
MTprefix=MTout
PTprefix=PTout
RAWHLTprefix=RAWHLTout
ESDprefix=ESDout
AODprefix=AODout

doMTPT=no
doRAWtoRAWHLT=no
doRAWtoESD=no
doRAWtoAOD=no
doESDtoAOD=no

for arg in $*; do
    echo $arg
    if [[ $arg == MTPT ]]; then
	doMTPT=yes
    elif [[ $arg == RAWtoRAWHLT ]]; then
	doRAWtoRAWHLT=yes
    elif [[ $arg == RAWtoESD  ]]; then
	doRAWtoESD=yes
    elif [[ $arg == RAWtoAOD ]]; then
	doRAWtoAOD=yes
    elif [[ $arg == ESDtoAOD ]]; then
	doESDtoAOD=yes
    fi
done

files=(
    #/pcatr-srv1/home/tkohno/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-9._0129.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0001.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0002.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0003.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0004.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0005.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0006.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0007.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0008.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0009.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0010.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0011.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0012.data
    /castor/cern.ch/grid/atlas/DAQ/2010/00166198/debug_L2HltError/data10_7TeV.00166198.debug_L2HltError.daq.RAW._lb0000._SFO-10._0013.data
)

a=
for f in $files; do
    a="${a},${f}"
done
#files=(${a[2,-1]})

function runMTPT() {
    inputBSFile=$1
    PTout=$2
    id=$3
    outputBSFile=$PTout
    MTout=MTout.$2
    if [[ -e trig.py ]]; then rm trig.py; fi
    if [[ -e $MTout ]]; then rm $MTout; fi
    if [[ -e $outputBSFile ]]; then rm $outputBSFile; fi
    if [[ $id -ge 3 ]]; then
	athenaMT.py -o $MTout -f $inputBSFile \
	    -J TrigConf::HLTJobOptionsSvc -b DBServer=TRIGGERDB:Instance=L2:DBSMKey=923:DBHLTPSKey=2340:DBLVL1PSKey=923 
	if [[ -e expert-monitoring.root ]]; then
	    mv expert-monitoring.root l2-expert-monitoring_${id}.root
	fi
    fi

    athenaPT.py -o $PTout -f ${MTout}-1._0001.data \
	-J TrigConf::HLTJobOptionsSvc -b DBServer=TRIGGERDB:Instance=EF:DBSMKey=923:DBHLTPSKey=2340:DBLVL1PSKey=923 

    if [[ -e expert-monitoring.root ]]; then
	mv expert-monitoring.root ef-expert-monitoring_${id}.root
    fi
#    athenaMT.py -o $MTout -f $inputBSFile \
#	-c 'setMenu="Physics_pp_v1";setLVL1XML="./LVL1config_Physics_pp_v1_15.6.9.28.xml";setupForMC=False' runHLT_standalone.py
#    athenaPT.py -o $PTout -f ${MTout}-1._0001.data \
#	-c 'setMenu="Physics_pp_v1";setLVL1XML="./LVL1config_Physics_pp_v1_15.6.9.28.xml";setupForMC=False' runHLT_standalone.py

}

function runRAWtoRAWHLT() {
    inputBSFile=$1
    outputBSFile=$2
    if [[ -e trig.py ]]; then rm trig.py; fi
    cat <<EOF > trig.py
from TriggerJobOpts.TriggerFlags import TriggerFlags
TriggerFlags.inputLVL1configFile="TriggerMenuXML/LVL1config_MC_pp_v1_15.6.9.23.1.xml"
TriggerFlags.inputHLTconfigFile="TriggerMenuXML/HLTconfig_MC_pp_v1_15.6.9.23.1.xml"
EOF
#    RAWtoRAWHLT_trf.py \
    Reco_trf.py \
	triggerConfig=MC_pp_v1 \
	inputBSFile=$inputBSFile \
	maxEvents=-1 \
	autoConfiguration=everything \
	outputBSFile=$outputBSFile \
	postInclude=trig.py 
}

function runRDOtoBSHLT() {
}

#ESDtoAOD_trf.py \
#Reco_trf.py \
#    inputESDFile=$inputESDFile \
#    maxEvents=5 \
#    autoConfiguration='everything' \
#    preInclude=RecExCommission/RecExCommission.py \
#    topOptions=RecExCommon_topOptions.py \
#    outputNTUP_TRIG=TrigNtuple.root


#    preExec='TriggerFlags.NtupleProductionFlags.ProductionLocation.set_Value_and_Lock("User")' \

function runESDtoNTUP_TRIG() {
    Reco_trf.py \
	inputESDFile=$inputESDFile \
	maxEvents=-1 \
	autoConfiguration=everything \
	outputAODFile=myAOD.pool.root \
	outputDESD_SGLELFile=myDESD_SGLEL.pool.root \
	outputDESD_MBIASFile=myDESD_MBIAS.pool.root \
	outputDESDM_TRACKFile=myDESDM_TRACK.pool.root \
	outputDESD_SGLMUFile=myDESD_SGLMU.pool.root \
	outputDESD_COLLCANDFile=myDESD_COLLCAND.pool.root \
	outputTAGFile=myTAG.root \
	outputDESDM_MUONFile=myDESDM_MUON.pool.root \
	outputDESD_PHOJETFile=myDESD_PHOJET.pool.root \
	outputDESDM_EGAMMAFile=myDESDM_EGAMMA.pool.root \
	outputTAG_COMMFile=myTAG_COMM.root \
	outputDESDM_CALJETFile=myDESDM_CALJET.pool.root \
	outputNTUP_MUONCALIBFile=myNTUP_MUONCALIB.root \
	outputNTUP_TRIGFile=myNTUP_TRIG.root \
	outputHISTFile=myHIST.root \
	outputDESD_METFile=myDESD_MET.pool.root \
	outputNTUP_EGAMMAFile=myNTUP_EGAMMA.root
}

((i = 0))
for f in $files; do
    echo "Processing file: '$f' ..."
    fin=$f
    fout=$f
    log=output_${i}.log
    if [[ -e $log ]]; then rm $log; fi
    #
    #echo "doMTPT=$doMTPT"
    #echo "doRAWtoESD=$doRAWtoESD"
    if [[ $doMTPT != no ]]; then
	echo "Run athenaMT/PT ..."
	fout=PTout.$i
	runMTPT $fin $fout $i >& $log
    fi
    if [[ $doRAWtoESD != no ]]; then
	echo "Doing RAWtoESD ..."
	fin=$fout
	fout=${fprefix}_${i}.ESD.pool.root
    elif [[ $doRAWtoAOD != no ]]; then
	echo "Doing RAWtoAOD ..."
	fin=$fout
	fout=${fprefix}_${i}.AOD.pool.root
	Reco_trf.py \
	    inputBSFile=${fin} \
	    maxEvents=-1 \
	    preInclude='trigconfig.py' \
	    autoConfiguration=everything \
	    outputESDFile=${fprefix}_${i}.ESD.pool.root \
	    outputAODFile=${fprefix}_${i}.AOD.pool.root >> $log
    fi
    (( i = $i + 1 ))
done


