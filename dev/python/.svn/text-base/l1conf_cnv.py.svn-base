#!/usr/bin/env python

import os
import sys
import re
import xml.dom.minidom

n_em_thr = 0
n_tau_thr = 0
n_jet_thr = 0
n_je_thr = 0
n_jf_thr = 0
n_jb_thr = 0
n_te_thr = 0
n_xe_thr = 0
n_mu_thr = 0

ClusterOff   = 255
IsolationOff = 63
JetOff       = 1023
EtSumOff     = 2047
EtMissOff    = 2895
JetEtOff     = 13286

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

def cableSlot(type):
    global ctpin_map
    slot = ''
    if type in ctpin_map.keys():
        slot = ctpin_map[type][0]
    return slot

def cableConnector(type):
    global ctpin_map
    connector = ''
    if type in ctpin_map.keys():
        connector = ctpin_map[type][1]
    return connector

def cableName(type):
    global ctpin_map
    slot = ''
    if type in ctpin_map.keys():
        slot = ctpin_map[type][2]
    return slot

def rangeBegin(mapping, type):
    offset = 0
    bitnum = 0
    if type in [ 'MUON', 'EM', 'TAU', 'JET' ]:
        offset = 0
        bitnum = 3
    elif type in ['JF' ]:
        offset = 0
        bitnum = 2
    elif type in ['JB' ]:
        offset = 8
        bitnum = 2
    elif type in ['JE' ]:
        offset = 24
        bitnum = 1
    elif type in ['JE' ]:
        offset = 24
        bitnum = 1
    elif type in ['TE' ]:
        offset = 0
        bitnum = 1
    elif type in ['XE' ]:
        offset = 4
        bitnum = 1
    elif type in ['JE' ]:
        offset = 24
        bitnum = 1
    print 'offset: ',offset, ' bitnum;',bitnum , 'mapping:',mapping,'type',type
    return (offset + mapping*bitnum)
        
    
def nextCtpid(type):
    global ctpid_em
    global ctpid_muon
    global ctpid_tau
    global ctpid_jet
    global ctpid_et
    global ctpid_other
    x = -1
    if type in [ 'EM' ]:
        x = ctpid_em
        ctpid_em += 1
    elif type in [ 'MUON' ]:
        x = ctpid_muon
        ctpid_muon += 1
    elif type in [ 'TAU' ]:
        x = ctpid_tau
        ctpid_tau += 1
    elif type in [ 'JET', 'JF', 'JB' ]:
        x = ctpid_jet
        ctpid_jet += 1
    elif type in [ 'XE', 'TE', 'JE' ]:
        x = ctpid_et
        ctpid_et += 1
    else:
        x = ctpid_other
        ctpid_other += 1
    return str(x)


def getGeVAttr(e, attr, def_value='', ignore=[]):
    x = getAttr(e, attr, def_value, ignore)
    x = x.replace('*GeV', '')
    ignorelist = []
    for a in ignore:
        ignorelist.append(str(a))
    if x in ignorelist:
        x = str(def_value)
    return x

def getAttr(e, attr, def_value='', ignore=[]):
    v = str(def_value)
    ignorelist = []
    for a in ignore:
        ignorelist.append(str(a))
    if e.hasAttribute(attr):
        v = e.getAttribute(attr)
        if v in ignorelist:
            v = str(def_value)
    return v

def comp_name(e1, e2):
    name1 = e1.getAttribute('name')
    name2 = e2.getAttribute('name')
    if name1 < name2:
        return -1
    elif name1 == name2:
        return 0
    else:
        return 1

def findConditions(e):
    conds = e.getElementsByTagName('TriggerCondition')
    nodes = e.getElementsByTagName('AND')
    nodes.extend(e.getElementsByTagName('OR'))
    nodes.extend(e.getElementsByTagName('NOT'))
    for node in nodes:
        conds.extend(findConditions(node))
    return conds

def findThreshold(name, thresholds):
    for thr in thresholds:
        if thr.getAttribute('name') == name:
            return thr
    return None

def itemType(e, all_thresholds):
    conds = findConditions(e)
    type = ''
    for cond in conds:
        thr_name = cond.getAttribute('triggerthreshold')
        thr = findThreshold(thr_name, all_thresholds)
        if len(type)==0:
            type = thr.getAttribute('type')
        elif type != thr.getAttribute('type'):
            type = ''
            break
    return type

def conditionElement(e):
    condition = xml.dom.minidom.Element(e.tagName)
    if e.tagName=='TriggerCondition':
        thr = getAttr(e, 'triggerthreshold')
        multi = getAttr(e, 'mult')
        condition.setAttribute('name', thr+'_x'+multi)
        condition.setAttribute('triggerthreshold', thr)
        condition.setAttribute('multi', multi)
    #
    childNodes = e.childNodes
    for child in childNodes:
        if child.nodeType!=xml.dom.Node.ELEMENT_NODE: continue
        a = conditionElement(child)
        condition.appendChild(a)
    return condition
        
def itemElement(e):
    item = xml.dom.minidom.Element('TriggerItem')
    item.setAttribute('name', getAttr(e, 'TI_ID', ''))
    childNodes = e.childNodes
    for child in childNodes:
        if child.nodeType!=xml.dom.Node.ELEMENT_NODE: continue
        a = conditionElement(child)
        item.appendChild(a)
    return item

def bitnumForThreshold(type):
     bitnum_map = {
        'EM': 3, 
        'TAU': 3, 
        'JET': 3, 
        'JE': 1, 
        'JF': 2,
        'JB': 2,
        'TE': 1, 
        'XE': 1, 
        'MUON': 3
        }
     if type in bitnum_map.keys():
         return bitnum_map[type]
     else:
         return 0
   
def oldToNewThresholdType(old_type):
    new_type = ''
    ttmap = {
        'EM': 'EM', 
        'HA': 'TAU', 
        'JE': 'JE', 
        'JT': 'JET', 
        'FR': 'JF',
        'FL': 'JB',
        'SM': 'TE', 
        'TM': 'XE', 
        'MU': 'MUON'
        }
    if old_type in ttmap.keys():
        new_type = ttmap[old_type]
    return new_type

def ttvElement(e, type):
    ttv = xml.dom.minidom.Element('TriggerThresholdValue')
    def_window = 0
    def_ptcut = 0
    def_isol = IsolationOff
    def_etamin = -49
    def_etamax = 49
    ttv.setAttribute('type', type)
    if type=='EM' or 'TAU':
        def_ptcut = ClusterOff
    elif type=='JET':
        def_ptcut = JetOff
        def_window = 8
    elif type == 'JF':
        def_ptcut = JetOff
        def_window = 4
        def_etamin = 0
    elif type == 'JB':
        def_ptcut = JetOff
        def_window = 4
        def_etamax = 0
    elif type == 'JE':
        def_ptcut = JetEtOff
    elif type == 'TE':
        def_ptcut = EtSummOff
    elif type == 'XE':
        def_ptcut = EtMissOff
        
    #
    ttv.setAttribute('thresholdval', getGeVAttr(e, 'thresholdval', def_ptcut))
    ttv.setAttribute('em_isolation',\
                     getGeVAttr(e, 'emisolation', def_isol, [999]))
    ttv.setAttribute('had_isolation',\
                     getGeVAttr(e, 'haisolation1', def_isol, [999]))
    ttv.setAttribute('had_veto', getGeVAttr(e, 'haisolation2',\
                                            def_isol, [999]))
    ttv.setAttribute('etamin', getAttr(e, 'etamin', def_etamin, [-5]))
    ttv.setAttribute('etamax', getAttr(e, 'etamax', def_etamax, [5]))
    ttv.setAttribute('phimin', getAttr(e, 'phimin', 0))
    ttv.setAttribute('phimax', getAttr(e, 'phimax', 64, [360]))
    ttv.setAttribute('window', getAttr(e, 'window', def_window))
    return ttv
    
def thresholdElement(e):
    global n_em_thr
    global n_tau_thr
    global n_jet_thr
    global n_jf_thr
    global n_jb_thr
    global n_je_thr
    global n_te_thr
    global n_xe_thr
    global n_mu_thr
    thr = xml.dom.minidom.Element('TriggerThreshold')
    thr.setAttribute('name', getAttr(e, 'name', ''))
    type = getAttr(e, 'type')
    type = oldToNewThresholdType(type)
    mapping = 0
    if type=='EM':
        mapping = n_em_thr
        n_em_thr += 1
    elif type=='TAU':
        mapping = n_tau_thr
        n_tau_thr += 1
    elif type=='JET':
        mapping = n_jet_thr
        n_jet_thr += 1
    elif type=='JE':
        mapping = n_je_thr
        n_je_thr += 1
    elif type=='JF':
        mapping = n_jf_thr
        n_jf_thr += 1
    elif type=='JB':
        mapping = n_jb_thr
        n_jb_thr += 1
    elif type=='TE':
        mapping = n_te_thr
        n_te_thr += 1
    elif type=='XE':
        mapping = n_xe_thr
        n_xe_thr += 1
    elif type=='MUON':
        mapping = n_mu_thr
        n_mu_thr += 1
    bitnum = bitnumForThreshold(type)
    if bitnum == 0:
        print 'Error unknown bitnum for threshold type ', type
    thr.setAttribute('type', type)
    thr.setAttribute('mapping', str(mapping))
    thr.setAttribute('active', '1')
    thr.setAttribute('bitnum', str(bitnum))
    sub = xml.dom.minidom.Element('Cable')
    sub.setAttribute('ctpin', cableSlot(type))
    sub.setAttribute('connector', cableConnector(type))
    sub.setAttribute('name', cableName(type))
    sub2 = xml.dom.minidom.Element('Signal')
    range_begin = rangeBegin(mapping, type)
    sub2.setAttribute('range_begin', str(range_begin))
    sub2.setAttribute('range_end', str(range_begin+bitnum-1))
    sub.appendChild(sub2)
    ttvs = e.getElementsByTagName('TriggerThresholdValue')
    for ttv in ttvs:
        e = ttvElement(ttv, type)
        thr.appendChild(e)
    thr.appendChild(sub)
    return thr

def prescaleSetElement():
    e = xml.dom.minidom.Element('PrescaleSet')
    for i in range(256):
        sub = xml.dom.minidom.Element('Prescale')
        sub.setAttribute('ctpid', str(i))
        text = xml.dom.minidom.Text()
        text.replaceWholeText('1')
        sub.appendChild(text)
        e.appendChild(sub)
    return e

def prioritySetElement():
    e = xml.dom.minidom.Element('PrioritySet')
    for i in range(256):
        sub = xml.dom.minidom.Element('Priority')
        sub.setAttribute('ctpid', str(i))
        text = xml.dom.minidom.Text()
        text.replaceWholeText('LOW')
        sub.appendChild(text)
        e.appendChild(sub)
    return e

def randomElement():
    e = xml.dom.minidom.Element('Random')
    e.setAttribute('rate1', '0')
    e.setAttribute('rate2', '0')
    return e

def deadtimeElement():
    e = xml.dom.minidom.Element('Deadtime')
    e.setAttribute('simple', '0')
    e.setAttribute('complex1_level', '0')
    e.setAttribute('complex1_rate', '0')
    e.setAttribute('complex2_level', '0')
    e.setAttribute('complex2_rate', '0')
    return e

def bunchGroupSetElement():
    e = xml.dom.minidom.Element('BunchGroupSet')
    return e

def prescaledClockElement():
    e = xml.dom.minidom.Element('PrescaledClock')
    e.setAttribute('clock1', '0')
    e.setAttribute('clock2', '0')
    return e

def muctpiElement():
    e = xml.dom.minidom.Element('MuctpiInfo')
    sub = xml.dom.minidom.Element('low_pt')
    text = xml.dom.minidom.Text()
    text.replaceWholeText('1')
    sub.appendChild(text)
    e.appendChild(sub)
    sub = xml.dom.minidom.Element('high_pt')
    text = xml.dom.minidom.Text()
    text.replaceWholeText('1')
    sub.appendChild(text)
    e.appendChild(sub)
    sub = xml.dom.minidom.Element('max_cand')
    text = xml.dom.minidom.Text()
    text.replaceWholeText('13')
    sub.appendChild(text)
    e.appendChild(sub)
    return e

def caloInfoElement():
    e = xml.dom.minidom.Element('CaloInfo')
    e.setAttribute('global_scale', '1.0')
    for i in range(12):
        sub = xml.dom.minidom.Element('JetWeight')
        sub.setAttribute('num', str(i+1))
        text = xml.dom.minidom.Text()
        text.replaceWholeText('0')
        sub.appendChild(text)
        e.appendChild(sub)
    return e

def usage():
    print "Usage: %s <menu_file> <thresholds_file> <output_file>" % sys.argv[0]
    
if __name__=='__main__':
    menu_file = 'LVL1triggermenuCSC-05-900GeV.xml'
    thr_file = 'LVL1triggerthresholdsCSC-05-900GeV.xml'
    config_file = 'abc.xml'
    if len(sys.argv) != 4:
        usage()
        sys.exit(1)
    if len(sys.argv) > 1:
        menu_file = sys.argv[1]
    if len(sys.argv) > 2:
        thr_file = sys.argv[2]
    if len(sys.argv) > 3:
        config_file = sys.argv[3]
    menu_doc = xml.dom.minidom.parse(menu_file)
    thr_doc = xml.dom.minidom.parse(thr_file)
    #
    config_doc = xml.dom.minidom.Document()
    l1config = xml.dom.minidom.Element('LVL1Config')
    trigger_menu = xml.dom.minidom.Element('TriggerMenu')
    thresholds = xml.dom.minidom.Element('TriggerThresholdList')
    #
    items = menu_doc.getElementsByTagName('TriggerItem')
    thrs = thr_doc.getElementsByTagName('TriggerThreshold')
    #
    print 'thrs size: ', len(thrs)
    thrs_out = []
    for thr in thrs:
        e = thresholdElement(thr)
        thrs_out.append(e)
    thrs_out.sort(comp_name)
    for e in thrs_out:
        thresholds.appendChild(e)
    #
    print 'items size: ', len(items)
    for (i, item) in enumerate(items):
        e = itemElement(item)
        e.setAttribute('ctpid', nextCtpid(itemType(e, thrs_out)))
        trigger_menu.appendChild(e)

    l1config.appendChild(trigger_menu)
    l1config.appendChild(thresholds)
    # Other stuffs
    l1config.appendChild(prescaleSetElement())
    l1config.appendChild(prioritySetElement())
    l1config.appendChild(randomElement())
    l1config.appendChild(bunchGroupSetElement())
    l1config.appendChild(prescaledClockElement())
    l1config.appendChild(muctpiElement())
    l1config.appendChild(caloInfoElement())
    l1config.appendChild(deadtimeElement())
    #
    config_doc.appendChild(l1config)
    fout = open(config_file, 'w')
    fout.write(config_doc.toprettyxml('  '))
    fout.close()

