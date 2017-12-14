#!/usr/bin/env python

import os
import sys
import re
import xml.dom.minidom

#-----------------------------------------------------------------------
# Inputs:
l1config_file='lvl1.xml'
#-----------------------------------------------------------------------

n_em_thr = 0
n_tau_thr = 0
n_jet_thr = 0
n_je_thr = 0
n_jf_thr = 0
n_jb_thr = 0
n_te_thr = 0
n_xe_thr = 0
n_mu_thr = 0

ClusterOff   = 'ClusterOff'
IsolationOff = 'IsolationOff'
JetOff       = 'JetOff'
EtSumOff     = 'EtSumOff'
EtMissOff    = 'EtMissOff'
JetEtOff     = 'JetEtOff'

ctpid_em = 0
ctpid_muon = 32
ctpid_tau = 64
ctpid_jet = 96
ctpid_et = 128
ctpid_other = 160

ctpin_map = {
    'EM': ('SLOT7', 'CON1', 'CP1'),
    'TAU': ('SLOT7', 'CON2', 'CP2'),
    'JET': ('SLOT8', 'CON0', 'JEP1'),
    'JE': ('SLOT8', 'CON0', 'JEP1'),
    'JF': ('SLOT8', 'CON1', 'JEP2'),
    'JB': ('SLOT8', 'CON1', 'JEP2'),
    'TE': ('SLOT8', 'CON2', 'JEP3'),
    'XE': ('SLOT8', 'CON2', 'JEP3'),
    'MUON': ('SLOT9', 'CON0', 'MU'),
    }

TPC='triggerPythonConfig'
thr_mappings = {
    'EM': [ [], 16], 
    'TAU': [ [], 8], 
    'JET': [ [], 8], 
    'JF': [ [], 4], 
    'JB': [ [], 4], 
    'JE': [ [], 4], 
    'TE': [ [], 4], 
    'XE': [ [], 8], 
    'MUON': [ [], 6]
    }

def writeThresholdList(doc, fout):
    global thr_mappings
    l1thrs = doc.getElementsByTagName('TriggerThreshold')
    for thr in l1thrs:
        name = thr.getAttribute('name')
        type = thr.getAttribute('type')
        mapping = 0
        slot = ''
        connector = ''
        active = 1
        
        if thr.hasAttribute('mapping'):
            mapping = thr.getAttribute('mapping')
        if mapping==-1:
            mapping_status = thr_mapping[type]
            choise = range(mapping_status[1])
            lambda 
            for a in mapping_status[0]:
                if a in choise
            mapping = 
        if thr.hasAttribute('slot'):
            slot = thr.getAttribute('slot')
        if thr.hasAttribute('connector'):
            connector = thr.getAttribute('connector')
        if thr.hasAttribute('active'):
            active = thr.getAttribute('active')
        fout.write("%s.addLvl1Threshold('%s','%s','%s','%s','%s','%s')\n" %
                   (TPC, name, type, mapping, slot, connector, active)
                   )
        

if __name__=='__main__':
    # fout = open('lvl1config.py', 'w')
    fout = sys.stdout
    fout.write('from TrigConfigSvc.TriggerPythonConfig import *\n')
    fout.write('\n')
    l1doc = xml.dom.minidom.parse(l1config_file)
    l1thrs = l1doc.getElementsByTagName('TriggerThresholdList')
    if len(l1thrs)==1:
        print 'hi'
        print 'hi2: ', type(l1thrs)
        writeThresholdList(l1thrs.item(0), fout)
    
    
