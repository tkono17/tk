#!/usr/bin/env python
#----------------------------------------------------------------------
# trigconf_htlseq.py
# ------------------
# Dumps the HLT sequences in a nice format from the XML file.
#----------------------------------------------------------------------

import os, sys
import re
import xml.dom.minidom
from trigconf_hltseq import *

gSeqNameMap = {}

def setupSeqNameMap():
    global gSeqNameMap
    gSeqNameMap = {
        '->TrigEFDsPhiPiFex->TrigEFDsPhiPiHypo': 'Seq_EFDsPhiPi', 
        '->TrigIDSCAN->muComb->MucombHypo': 'Seq_IDSCAN_muon', 
        '->TrigSiTrack->TrigT2HistoPrmVtx->TrigIDSCAN->TrigT2HistoPrmVtx->TrigBjetFex->TrigBjetHypo': 'Seq_Bjet', 
        '->T2CaloEgamma': 'Seq_L2CaloFex_egamma', 
        '->MooHLTAlgo->MooHLTAlgo->MooHLTAlgo->TrigMooreHypo': 'Seq_EF_muon', 
        '->PESA::TrigSpacePointCounter->PESA::TrigSpacePointCounterHypo': 'Seq_minbiasSP', 
        '->TrigIDSCAN->TrigSiTrack->muComb->MucombHypo': 'Seq_SiTrack_muon', 
        '->InDet::Pixel_TrgClusterization->InDet::SCT_TrgClusterization->InDet::TRT_TrgRIO_Maker->InDet::PRD_TrigMultiTruthMaker->InDet::SiTrigSpacePointFinder->InDet::SiTrigSPSeededTrackFinder->InDet::InDetTrigAmbiguitySolver->InDet::TRT_TrigTrackExtensionAlg->InDet::InDetTrigExtensProcessor->InDet::InDetTrigDetailedTrackTruthMaker->InDet::TrigVxPrimary->InDet::TrigParticleCreator->InDet::TrigTrackParticleTruthMaker->TrigEFTrackHypo': 'Seq_EFID4', 
        '->TrigL2JpsieeFex->TrigL2JpsieeHypo': 'Seq_L2Jpsiee', 
        '->TrigIDSCAN->TrigDiMuonFast->TrigL2DiMuHypo': 'Seq_L2DiMuon', 
        '->TrigL2JpsieeFex': 'Seq_L2JpsieeFex', 
        '->TrigTauRec->EFTauHypo': 'Seq_EF_tau', 
        '->TrigIDSCAN->T2IDTauHypo': 'Seq_L2ID_tau', 
        '->TrigL2BMuMuXFex->TrigL2BMuMuXHypo': 'Seq_L2BMuMuX', 
        '->T2TauFinal->T2TauHypo': 'Seq_L2_tau', 
        '->TrigCaloCellMaker': 'Seq_CaloCellMaker', 
        '->TrigCaloCellMaker->TrigCaloTowerMaker->TrigCaloClusterMaker': 'Seq_CaloClusterMaker', 
        '->TrigL2BMuMuFex->TrigL2BMuMuHypo': 'Seq_L2BMuMu', 
        '->OverlapRemoval': 'Seq_overlapRemoval', 
        '->TrigEgammaRec->TrigEFEgammaHypo': 'Seq_egammaRec', 
        '->TrigL2DielectronMassFex->TrigL2DielectronMassHypo': 'Seq_L2DiElectron', 
        '->T2CaloJet->TrigL2JetHypo': 'Seq_L2Calo_jet', 
        '->TrigIDSCAN': 'Seq_IDSCAN', 
        '->TrigL2PhotonFex->TrigL2PhotonHypo': 'Seq_L2_photon', 
        '->PESA::newDummyAlgoScan->TrigIDSCAN': 'Seq_IDSCAN_FS', 
        '->muIso->MuisoHypo': 'Seq_muIsol', 
        '->TrigL2DsPhiPiFex->TrigL2DsPhiPiHypo': 'Seq_L2DsPhiPi', 
        '->TrigL2IDCaloFex->TrigL2IDCaloHypo': 'Seq_L2IDCalo', 
        '->T2CaloTau->T2CaloTauHypo': 'Seq_L2Calo_tau', 
        '->muFast->MufastHypo': 'Seq_muFast', 
        '->PESA::T2MissingET->TrigEFMissingETHypo': 'Seq_L2_MET', 
        '->TrigIDSCAN->TrigSiTrack': 'Seq_L2ID', 
        '->EFMissingET->TrigEFMissingETHypo': 'Seq_EF_MET', 
        '->TrigCaloCellMaker->TrigCaloTowerMaker->TrigJetRec->TrigEFJetHypo': 'Seq_EFCalo_jet', 
        '->InDet::Pixel_TrgClusterization->InDet::SCT_TrgClusterization->InDet::TRT_TrgRIO_Maker->InDet::PRD_TrigMultiTruthMaker->InDet::SiTrigSpacePointFinder->InDet::SiTrigSPSeededTrackFinder->InDet::InDetTrigAmbiguitySolver->InDet::TRT_TrigTrackExtensionAlg->InDet::InDetTrigExtensProcessor->InDet::InDetTrigDetailedTrackTruthMaker->InDet::TrigParticleCreator->InDet::TrigTrackParticleTruthMaker': 'Seq_EFID1', 
        '->TrigEgammaRec->TrigEFPhotonHypo': 'Seq_EF_photon', 
        '->DummyFEX': 'Seq_dummy', 
        '->InDet::Pixel_TrgClusterization->InDet::SCT_TrgClusterization->InDet::TRT_TrgRIO_Maker->InDet::PRD_TrigMultiTruthMaker->InDet::SiTrigSpacePointFinder->InDet::SiTrigSPSeededTrackFinder->InDet::InDetTrigAmbiguitySolver->InDet::TRT_TrigTrackExtensionAlg->InDet::InDetTrigExtensProcessor->InDet::InDetTrigDetailedTrackTruthMaker->InDet::TrigVxPrimary->InDet::TrigParticleCreator->InDet::TrigTrackParticleTruthMaker->TrigT2HistoPrmVtx->TrigBjetFex->TrigBjetHypo': 'Seq_EFID2', 
        '->T2CaloEgamma->TrigL2CaloHypo': 'Seq_L2Calo_egamma', 
        '->InDet::Pixel_TrgClusterization->InDet::SCT_TrgClusterization->InDet::TRT_TrgRIO_Maker->InDet::PRD_TrigMultiTruthMaker->InDet::SiTrigSpacePointFinder->InDet::SiTrigSPSeededTrackFinder->InDet::InDetTrigAmbiguitySolver->InDet::TRT_TrigTrackExtensionAlg->InDet::InDetTrigExtensProcessor->InDet::InDetTrigDetailedTrackTruthMaker->InDet::TrigVxPrimary->InDet::TrigParticleCreator->InDet::TrigTrackParticleTruthMaker': 'Seq_EFID3', 
        }

i_unknown_seq_counter=0
def seqClassName(s):
    global i_unknown_seq_counter
    if s in gSeqNameMap.keys():
        return gSeqNameMap[s]
    else:
        s2 = 'Seq_unknown%d' % i_unknown_seq_counter
        print '# Unknown sequence type: ', s
        print '# Naming it now as %s' % s2
        i_unknown_seq_counter += 1
        gSeqNameMap[s] = s2
        return s2

def chainTopology(chain_type):
    # topologies: empty, N->N->...
    re_stepmulti = re.compile('\([\w,]+\)')
    re_stepmulti2 = re.compile('step(\d+),x(\d+)')
    words = re_stepmulti.findall(chain_type)
    ntes_in_step = []
    for w in words:
        mg = re_stepmulti2.search(w)
        if mg:
            step = int(mg.group(1))
            multi = int(mg.group(2))
            if step >= len(ntes_in_step):
                ntes_in_step.append(multi)
            else:
                ntes_in_step[step] += multi
    topo = ''
    for s in ntes_in_step:
        topo = '%s-%d' % (topo, s)
    if topo.startswith('-'): topo = topo[1:]
    return topo
                
def chainType(chain_rep, seq_reps, no_duplicate=True):
    # chain_rep: [chain_name, chain_counter, lower_chain,
    #              [ [te1], [te2a, te2b], ...] ]
    chtype = ''
    seqtype_to_multi = {}
    seqs = []
    seqtype_to_step = {}
    for (istep, tes) in enumerate(chain_rep[3]):
        for te in tes:
            seqtype = ''
            for seq in seq_reps:
                if te == seq[2]:
                    seqtype = seqType(seq)
                    break
            if not no_duplicate: seqtype = '%s_step%d' % (seqtype, istep)
            if seqtype in seqs:
                if seqtype_to_step[seqtype] == istep:
                    seqtype_to_multi[seqtype] += 1
            elif seqtype != '':
                seqtype_to_step[seqtype] = istep
                seqtype_to_multi[seqtype] = 1
                seqs.append(seqtype)
    for seq in seqs:
        n = seqtype_to_multi[seq]
        chtype += '%s(step%d,x%d)' % (seq, seqtype_to_step[seq], n)
    return chtype
    
def allChainTypes(chain_reps, seq_reps):
    unique_chain_types = []
    for c in chain_reps:
        ctype = chainType(c, seq_reps)
        if ctype not in unique_chain_types:
            unique_chain_types.append(ctype)
    return unique_chain_types

def topoType(topo):
    # empty, single, 1toN, Nto1, NtoN, other
    topotype = 'empty'
    words = re.compile('\d+').findall(topo)
    n_prev = -1
    n_largest = -1
    n_current = -1
    is_empty = True
    always_one = True
    always_same = True
    always_same_from2 = True
    is_decreasing = True
    is_increasing = True
    is_decreasing_from2 = True
    for (i, w) in enumerate(words):
        is_empty = False
        n_current = int(w)
        if n_current != 1: always_one = False
        if n_current > n_largest: n_largest = n_current
        if n_prev >= 0 and n_prev != n_current:
            always_same = False
        if i >= 2 and n_prev != n_current:
            always_same_from2 = False
        if n_prev >= 0 and n_prev < n_current:
            is_decreasing = False
        if n_prev >= 0 and n_prev > n_current:
            is_increasing = False
        if i >= 2 and n_prev < n_current:
            is_decreasing_from2 = False
        n_prev = n_current
    if len(words)<3: is_decreasing_from2 = False
    #
    if is_empty:
        topotype = 'empty'
    elif always_one:
        topotype = 'single'
    elif n_largest>1 and n_current==1:
        if is_decreasing_from2 and int(words[0]) == 1:
            topotype = 'Nto1_startIs1'
        else:
            topotype = 'Nto1'
    elif always_same:
        topotype = 'NtoN'
    elif always_same_from2 and int(words[0])==1:
        topotype = 'NtoN_startIs1'
    elif is_decreasing:
        topotype = 'NtoN-'
    elif is_increasing:
        topotype = 'NtoN+'
    elif is_decreasing_from2 and int(words[0]) == 1:
        topotype = 'NtoN-_startIs1'
    elif is_decreasing_from2 and len(words)>2:
        topotype = 'NtoN-_from2'
    else:
        topotype = 'other'
        
    return topotype
def dumpChainDefs(chain_reps, seq_reps, lower_out_tes):
    # chains = allChainTypes(chain_reps, seq_reps)
    re_stepmulti = re.compile('\((step\d+,x\d+)\)')
    re_stepmulti2 = re.compile('step(\d+),x(\d+)')
    chain_box = []
    for (ic, chain) in enumerate(chain_reps):
        c = chainType(chain, seq_reps, True)
        if c in chain_box: continue
        else: chain_box.append(c)
        #
        c2 = chainType(chain, seq_reps, False)
        single_obj = False
        words = re_stepmulti.findall(c)
        # print c
        single_obj = True
        for xy in words:
            steps = []
            mg2 = re_stepmulti2.match(xy)
            if mg2:
                (step, multi) = mg2.groups()
                step = int(step)
                multi = int(multi)
                if step in steps or multi > 1:
                    single_obj = False
                    break
                else:
                    steps.append(step)
        topo = chainTopology(c)
        topo2 = chainTopology(c2)
        print '# Chain type: %s' % c
        print '# topology(algo): %20s: %-20s' % (topo, topoType(topo))
        print '# topology(TE)  : %20s: %-20s' % (topo2, topoType(topo2))
        if single_obj:
            dumpChainDef(c, 'SingleObjChain%d' % ic)
            print '\n'
        else:
            print '# Not a single object chain: %s' % c
    pass

def dumpChainDef(c, cname):
    re_multi = re.compile('\((step\d+,x\d+)\)')
    (c2, n) = re_multi.subn(',', c)
    seqs = filter(lambda x: x!='', c2.split(','))
    print '# %s' % cname
    print 'class %s(HltChain):' % cname
    print '    def __init__(self, name, counter, lower_chain, '
    print "                 input_te, sig_id='', params=[]): "
    print '        HltChain.__init__(self, name, counter, lower_chain)'
    for (i, s) in enumerate(seqs):
        if i == 0:
            te = 'input_te'
            suffix = "sig_id"
        elif i == len(seqs)-1:
            te = "seq%d.outputTE" % (i-1)
            suffix = 'sig_id'
        else:
            te = "seq%d.outputTE" % (i-1)
            suffix = "sig_id"
        print '        seq%d = %s(SeqConfig([], %s, %s))' % \
              (i, seqClassName(s), te, suffix)
    print '        self.steps = ['
    for (i, s) in enumerate(seqs):
        print '            seq%d, ' % i
    print '        ]'
    print '        self.setParams(params)'
    for i in range(len(seqs)):
        a, b = '', ''
        if i == 0: a += 'def setSeqConfigs('
        else: a = '                  '
        if i != len(seqs)-1: b = ', '
        else: b = '):'
        print '    %sseqConfig%d%s' % (a, i, b)
    print '        self.steps = ['
    for (i, s) in enumerate(seqs):
        print '            %s(seqConfig%d), ' % (seqClassName(s), i)
    print '        ]'
    print '        return self'
    pass

def readChainReps(doc):
    chs = doc.getElementsByTagName('CHAIN')
    l2chain_reps = []
    efchain_reps = []
    for c in chs:
        tmp_tes = []
        slist = c.getElementsByTagName('SIGNATURE_LIST')
        if len(slist) != 1:
            print '# Number of SIGNATURE_LIST under CHAIN is not one, %s' %\
                  c.getAttribute('chain_name')
            continue
        sigs = slist[0].getElementsByTagName('SIGNATURE')
        for s in sigs:
            tes = s.getElementsByTagName('TRIGGERELEMENT')
            tmp2 = []
            for te in tes:
                tmp2.append(te.getAttribute('te_name'))
            tmp_tes.append(tmp2)
        tmp = [ c.getAttribute('chain_name'), c.getAttribute('chain_counter'),
                c.getAttribute('lower_chain_name'), tmp_tes ]
        if c.getAttribute('level') == 'L2':
            l2chain_reps.append(tmp)
        elif c.getAttribute('level') == 'EF':
            efchain_reps.append(tmp)
        else:
            print '# unknown level of chain: ', c.getAttribute('chain_name')
    return (l2chain_reps, efchain_reps)

def dumpSeqDefs(unique_seqs):
    """Dump the definition of sequences"""
    for s in unique_seqs:
        tein = seqClassName(s).replace('Seq_', '') + '_in'
        teout = seqClassName(s).replace('Seq_', '') + ''
        dumpSeqDef(s, seqClassName(s), tein, teout)
        print '\n'
        pass
    pass

def dumpSeqDef(seqtype, cname, tein_base, teout_base):
    """Dump the definition of a sequence"""
    print 'class %s(HltSeq): ' % cname
    print "    inputTE_base = '%s'" % tein_base
    print "    outputTE_base = '%s'" % teout_base
    print '    def __init__(self, seqConfig): '
    print '        HltSeq.__init__(self)'
    print '        self.inputTE = seqConfig.inputTE or %s.inputTE_base' % \
          (cname)
    print '        self.outputTE = %s.outputTE_base + seqConfig.sig_id' % \
          (cname)
    print '        self.algorithms = ['
    print '            # List of algorithms for this sequence'
    print '            # Use appropriate configurables to get default parameters'
    algos = seqtype.split('->')
    algos = filter(lambda x: x!='', algos)
    for (i, algo) in enumerate(algos):
        algo_name = algo.replace(':', '_')
        inst_name = algo_name
        suffix = ''
        if i == len(algos)-1: suffix = '+seqConfig.sig_id'
        print "            %s('%s'%s), " % (algo_name, inst_name, suffix)
        pass
    print '            ]'
    pass

def dumpUnknownSeqs():
    for (s, n) in gSeqNameMap.iteritems():
        if n.find('unknown') >= 0:
            algos = s.split('->')
            n.rstrip('\n')
            print 'def %s(HltSeq):' % n
            for a in algos:
                if len(a)>0: print '    %s' % a
            print '\n'
    
if __name__=='__main__':
    #hltxml = '/space2/tkohno/work/FDR2/MenuXML/HLTconfig_default_13.0.40.4.xml'
    hltxml = '/space2/tkohno/athena/14.X.0/Trigger/TriggerCommon/TriggerMenuXML/data/HLTconfig_default_14.1.0.xml'
    hltdoc = xml.dom.minidom.parse(hltxml)
    
    seq_reps = readSeqReps(hltdoc)
    (l2chain_reps, efchain_reps) = readChainReps(hltdoc)

    unique_seqs = allSeqTypes(seq_reps)
    i=0
    for s in unique_seqs:
        if s not in gSeqNameMap.keys():
            gSeqNameMap[s] = 'Seq%d' % i
            i += 1
    setupSeqNameMap()
    print '# len: ', len(gSeqNameMap)
    seqnames = gSeqNameMap.values()
    seqnames.sort()
##     for s in seqnames:
##         print s
##         pass
    
    print 'from HltConfig import *'
    hypo_packages = [
        'from TrigBjetHypo.TrigBjetHypoConf import *', 
        'from TrigBphysHypo.TrigBphysHypoConf import *', 
        'from TrigEgammaHypo.TrigEgammaHypoConf import *', 
        'from TrigJetHypo.TrigJetHypoConf import *', 
        'from TrigL2CosmicMuonHypo.TrigL2CosmicMuonHypoConf import *', 
        'from TrigMissingETHypo.TrigMissingETHypoConf import *', 
        'from TrigMultiVarHypo.TrigMultiVarHypoConf import *', 
        'from TrigMuonHypo.TrigMuonHypoConf import *', 
        'from TrigTauHypo.TrigTauHypoConf import *',

        'from TrigCaloRec.TrigCaloRecConf import *', 
        'from TrigCaloRinger.TrigCaloRingerConf import *', 
        'from TrigDiMuon.TrigDiMuonConf import *', 
        'from TrigEFIDCosmic.TrigEFIDCosmicConf import *', 
        'from TrigEFMissingET.TrigEFMissingETConf import *', 
        'from TrigEgammaRec.TrigEgammaRecConf import *', 
        'from TrigGenericAlgs.TrigGenericAlgsConf import *', 
        'from TrigIDSCAN.TrigIDSCANConf import *', 
        'from TrigJetRec.TrigJetRecConf import *', 
        'from TrigL2CosmicCombined.TrigL2CosmicCombinedConf import *', 
        'from TrigL2CosmicMuon.TrigL2CosmicMuonConf import *', 
        'from TrigL2MissingET.TrigL2MissingETConf import *', 
        'from TrigMinBias.TrigMinBiasConf import *', 
        'from TrigMoore.TrigMooreConf import *', 
        'from TrigmuComb.TrigmuCombConf import *', 
        'from TrigmuFast.TrigmuFastConf import *', 
        'from TrigmuIso.TrigmuIsoConf import *', 
        'from TrigSiTrack.TrigSiTrackConf import *', 
        'from TrigT2CaloCommon.TrigT2CaloCommonConf import *', 
        'from TrigT2CaloCosmic.TrigT2CaloCosmicConf import *', 
        'from TrigT2CaloEgamma.TrigT2CaloEgammaConf import *', 
        'from TrigT2CaloJet.TrigT2CaloJetConf import *', 
        'from TrigT2CaloTau.TrigT2CaloTauConf import *', 
        'from TrigT2HistoPrmVtx.TrigT2HistoPrmVtxConf import *', 
        'from TrigT2IDTau.TrigT2IDTauConf import *', 
        'from TrigT2InDetMonitoring.TrigT2InDetMonitoringConf import *', 
        'from TrigT2MinBias.TrigT2MinBiasConf import *', 
        'from TrigT2Tau.TrigT2TauConf import *', 
        'from TrigTauRec.TrigTauRecConf import *', 
        'from TrigTileMuId.TrigTileMuIdConf import *', 
        'from TrigTRTxK.TrigTRTxKConf import *', 
        ]
    for pack in hypo_packages:
        print pack

    print '# Number of sequence types: ', len(unique_seqs)
    dumpSeqDefs(unique_seqs)

    print '# Number of L2 chains: ', len(l2chain_reps)
    dumpChainDefs(l2chain_reps, seq_reps, [])
    l2out_tes = []
    for c in l2chain_reps:
        [ l2out_tes.extend(x) for x in c[3]]

    print '# Number of EF chains: ', len(efchain_reps)
    dumpChainDefs(efchain_reps, seq_reps, l2out_tes)
    dumpUnknownSeqs()
    
