#!/usr/bin/env zsh

trigger_tests=(
    AthenaTrigRDO
    AthenaP1RDO
#     AthenaTrigRDO_leakcheck
#     CaloAthenaTrigRDO
#     IDAthenaTrigRDO
#     IDAthenaTrigRDO_preRTTtest
#     MuonAthenaTrigRDO
#     ElectronSliceAthenaTrigRDO
#     PhotonSliceAthenaTrigRDO
#     EgammaSliceAthenaTrigRDO_Lumi1E31
#     MuonSliceAthenaTrigRDO
#     TauSliceAthenaTrigRDO
#     JetSliceAthenaTrigRDO
#     METSliceAthenaTrigRDO
#     METSliceAthenaTrigRDO_nofastCalo
#     BphysicsSliceAthenaTrigRDO
#     BphysicsSliceAthenaTrigRDO_Kstar
#     BphysicsSliceAthenaTrigRDO_noMuon
#     BjetSliceAthenaTrigRDO
#     CosmicsSliceAthenaTrigRDO
#     MinBiasSliceAthenaTrigRDO
#     AthenaTrigBS_standalone
#     AthenaTrigRDO_standalone
#     AthenaTrigRDO_blackholes
#     LVL1CTPAthenaTrigRDO
#     LVL1CTPPrescaleAthenaTrigRDO
#     LVL1CTPCaloAthenaTrigRDO
#     LVL1CTPMuonAthenaTrigRDO
#     AthenaXMLConfigRDO
#     AthenaDBConfigRDO
#     AthenaTrigRDO_default
#     AthenaTrigRDO_noEF
#     AthenaTrigRDO_noFPE
#     AthenaTrigRDO_StatusCodes
#     AthenaTrigRDO_chainOrderDescend
#     AthenaTrigRDO_chainOrderAscend
#     standalone_cosmic
#     AthenaTrigRDO_MC_lumi1E31
#     AthenaTrigRDO_MC_lumi1E31_no_prescale
#     AthenaTrigRDO_Physics_lumi1E31
#     AthenaTrigRDO_Physics_lumi1E31_no_prescale
#     AthenaTrigRDO_MC_lumi1E32_no_prescale
#     AthenaTrigRDO_MC_lumi1E33_no_prescale
#     AthenaTrigRDO_Physics_lumi1E32_no_prescale
#     AthenaTrigRDO_Physics_lumi1E33_no_prescale
#     AthenaTrigRDO_Physics_lumi1E34_no_prescale
#     AthenaTrigRDO_Physics_lumi1E31_simpleL1Calib 
#     AthenaTrigRDO_MC_lumi1E31_simpleL1Calib 
#     AthenaTrigRDO_Physics_lumi1E31_simpleL1Calib_no_prescale 
#     AthenaTrigRDO_MC_lumi1E31_simpleL1Calib_no_prescale
#     AthenaTrigRDO_cosmic_default
#     AthenaTrigRDO_InitialBeam_default
#     AthenaTrigRDO_MC_InitialBeam_v1_no_prescale
#     pureNewSteering
#     pureNewSteering_ecodes
#     pureNewSteering_prescaling
)

analysis_tests=(
"AthenaTrigRDOtoESDAOD"
"AthenaTrigRDOtoBS"
"AthenaTrigRDOtoCBNT"
"AthenaTrigRDOtoTAG"
"AthenaTrigRDOtoAOD"
"AthenaTrigAOD_rerunHYPO"
"AthenaTrigAOD_rerunHYPO_highETthr"
"AthenaTrigAOD_rerunHYPO_tunedCuts"
"AthenaTrigRDO_TDT"
"RootTrigAOD_TDT"
"AthenaTrigAOD_TDT_fixedAOD"
"RootTrigAOD_TDT_fixedAOD"
"AthenaTrigAOD_TrigDecTool"
"AthenaTrigAOD_TrigDecTool_fixedAOD"
"AthenaTrigAOD_rerun_TrigDecTool"
"AthenaTrigAOD_rerun_highETthr_TrigDecTool"
"AthenaTrigAOD_rerun_tunedCuts_TrigDecTool"
"AthenaTrigAOD_rerun_compareCounts"
"AthenaTrigAOD_HLTMonitoring"
"AthenaTrigAOD_HLTMonitoring_fixedAOD"
"AthenaTrigBStoESD"
"AthenaTrigAOD_TrigEDMCheck"
"AthenaTrigAOD_TrigEDMCheck_fixedAOD"
"ElectronSliceAthenaTrigRDOtoESDAOD"
"EgammaSliceAthenaTrigRDOtoESDAOD_Lumi1E31"
"MuonSliceAthenaTrigRDOtoESDAOD"
"TauSliceAthenaTrigRDOtoESDAOD"
"JetSliceAthenaTrigRDOtoESDAOD"
"METSliceAthenaTrigRDOtoESDAOD"
"BphysicsSliceAthenaTrigRDOtoESDAOD"
"BjetSliceAthenaTrigRDOtoESDAOD"
"MinBiasSliceAthenaTrigRDOtoESDAOD"

"AthenaTrigAOD_UnslimVal"
"AthenaTrigAODtoAOD_TrigNavSlimming"
"AthenaTrigAOD_TrigSlimValidation"
"AthenaTrigAODtoAOD_TrigNavSqueeze"
"AthenaTrigAOD_TrigSqueezeValidation"
"AthenaTrigAOD_Trigslimval"
"BackCompAthenaTrigBStoESDAOD_14.2.2X"

"BackCompAthenaTrigAOD_14.2.2X_TrigDecTool"
"BackCompAthenaTrigAOD_14.2.2X_TrigEDMCheck"
"BackCompAthenaTrigAOD_14.2.2X_rerunHYPO"
"atn_xml_summary_table"
)

function run_test() {
    test=$1
    rundir=$test
    conf=$2
    # trigtest.pl --test AthenaModernRDO --rundir AthenaModernRDO --conf TriggerTest.conf
    trigtest.pl --test $test --rundir $rundir --conf $conf
}

tests=()
conf=""
while getopts 'la:t:h' opt $*; do
    case $opt in
	l)
	    for t in $trigger_tests; do
		echo "$t"
	    done
	    ;;
	a)
	    if [[ $OPTARG == 'ALL' ]]; then
		tests=($analysis_tests)
	    else
		tests=(`echo $OPTARG | sed "s/,/ /g"`)
	    fi
	    conf="TrigAnalysisTest.conf";;
	t)
	    if [[ $OPTARG == 'ALL' ]]; then
		tests=($trigger_tests)
	    else
		tests=(`echo $OPTARG | sed "s/,/ /g"`)
	    fi
	    conf="TriggerTest.conf"
	    ;;
	h)
	    echo "Usage: $0 [-l,-t <test1,test2,...>, -h]"
	    ;;
    esac
done

if [[ ${#tests} -gt 0 && $conf != "" ]]; then
    for t in $tests; do
	run_test $t $conf
    done
fi

