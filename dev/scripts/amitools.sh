#!/usr/bin/env zsh

ami_datasetOfNameTypeRelease () {
    if [[ $# < 3 ]] then
	echo "Usage: ami_datasetOfNameTypeRelease <pattern> <type> <release> <trf_release>"
	echo "------"
	echo "Example: > ami_datasetOfNameTypeRelease '%T1_McAtNlo%' AOD 14.2.21 14.2.21"
	return 1;
    fi
    name=$1
    data_type=$2
    release=$3
    trf_release=$release
    if [[ $# == 4 ]]; then
	trf_release=$4;
    fi


    python /afs/cern.ch/atlas/software/builds/nightlies/dev/AtlasCore/rel_2/Database/Bookkeeping/AMIClients/pyAMI/python/pyAMI.py BrowseSQLQuery \
	-amiAdvanced="ON" \
	-amiLang="english" \
	-gLiteEntity="dataset" \
	-gLiteQuery="SELECT dataset.logicalDatasetName ,dataset.dataType ,dataset.physicsCategory ,dataset.physicsSubcategory ,dataset.AtlasRelease ,dataset.prodsysStatus ,dataset.principalPhysicsGroup ,dataset.datasetNumber ,dataset.version ,dataset.productionStep WHERE logicalDatasetName LIKE '${name}' AND (amiStatus!='TRASHED') AND (dataset.dataType='${data_type}') AND (AtlasRelease='${release}' or TransformationPackage='${trf_release}')" \
	-processingStep="production" \
	-project="csc" \
	-sql="SELECT dataset.logicalDatasetName ,dataset.dataType ,dataset.physicsCategory ,dataset.physicsSubcategory ,dataset.AtlasRelease ,dataset.prodsysStatus ,dataset.principalPhysicsGroup ,dataset.datasetNumber ,dataset.version ,dataset.productionStep ,'csc' as PROJECT,'production' as PROCESS, 'dataset' as AMIENTITYNAME, dataset.identifier as AMIELEMENTID FROM dataset WHERE ((((dataset.identifier IN (SELECT dataset.identifier FROM dataset WHERE dataset.logicalDatasetName LIKE '${name}')) AND (dataset.identifier IN (SELECT dataset.identifier FROM dataset WHERE dataset.amiStatus != 'TRASHED'))) AND (dataset.identifier IN (SELECT dataset.identifier FROM dataset WHERE dataset.dataType = '${data_type}'))) AND ((dataset.identifier IN (SELECT dataset.identifier FROM dataset WHERE dataset.AtlasRelease = '${release}')) OR (dataset.identifier IN (SELECT dataset.identifier FROM dataset WHERE dataset.TransformationPackage = '${trf_release}'))))"
}
