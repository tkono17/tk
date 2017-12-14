#!/usr/bin/env python
#------------------------------------------------------------
# tm_xml2list.py
#------------------------------------------------------------

import os, sys
import re
import xml.dom.minidom

def usage():
    print 'Usage: %s <lvl1_xml> <htl_xml>' % sys.argv[0]

class Menu:
    def __init__(self):
        pass
    def setL1Thresholds(self, thrs):
        self.l1_thrs = thrs
    def setL1Items(self, items):
        self.l1_items = items
    def setL2Chains(self, chains):
        self.l2_chains = chains
    def setEFChains(self, chains):
        self.ef_chains = chains
    def printIt(self):
        def sort_by_name(x1, x2):
            if n1 < n2: return -1
            elif n1 > n2: return 1
            else: return 0
        self.l1_items.sort(sort_by_name)
        self.l2_chains.sort(sort_by_name)
        self.ef_chains.sort(sort_by_name)
        for (type, mapping, x) in self.l1_thrs:
            print '%-10s %-5s %2d %-50s' % ('(A) L1_THR', type, mapping, x)
        for (id, x) in self.l1_items:
            print '%-10s %04d %-50s' % ('(B) L1_ITEM', id, x)
        for (id, x) in self.l2_chains:
            print '%-10s %04d %-50s' % ('(C) L2_CHAIN', id, x)
        for (id, x) in self.ef_chains:
            print '%-10s %04d %-50s' % ('(D) EF_CHAIN', id, x)

def readL1XML(xmlfile, menu):
    doc = xml.dom.minidom.parse(xmlfile)

    l1_thrs = doc.getElementsByTagName('TriggerThreshold')
    thrlist = []
    for x in l1_thrs:
        thrlist.append( (x.getAttribute('type'),
                         int(x.getAttribute('mapping')),
                         x.getAttribute('name')))
    menu.setL1Thresholds(thrlist)

    l1_items = doc.getElementsByTagName('TriggerItem')
    itemlist = []
    for x in l1_items:
        itemlist.append( (int(x.getAttribute('ctpid')),
                          x.getAttribute('name')))
    menu.setL1Items(itemlist)

def readHLTXML(xmlfile, menu):
    doc = xml.dom.minidom.parse(xmlfile)

    chains = doc.getElementsByTagName('CHAIN')
    l2_chainlist = []
    ef_chainlist = []
    for x in chains:
        chain = (int(x.getAttribute('chain_counter')),
                 x.getAttribute('chain_name'))
        level = x.getAttribute('level')
        if level == 'L2': l2_chainlist.append(chain)
        elif level == 'EF': ef_chainlist.append(chain)
    menu.setL2Chains(l2_chainlist)
    menu.setEFChains(ef_chainlist)


def createMenu(l1xml, hltxml):
    menu = Menu()
    readL1XML(l1xml, menu)
    readHLTXML(hltxml, menu)
    return menu
    
if __name__ == '__main__':
    if len(sys.argv) != 3 and False:
        usage()
        sys.exit(1)
    l1xml = '/space2/tkohno/athena/14.X.0/Trigger/TriggerCommon/TriggerMenuXML/data/LVL1config_lumi1E32_13.0.40.4.xml'
    hltxml = '/space2/tkohno/athena/14.X.0/Trigger/TriggerCommon/TriggerMenuXML/data/HLTconfig_lumi1E32_13.0.40.4.xml'
    if len(sys.argv)==1:
        usage()
        sys.exit(1)
    if len(sys.argv)>1: l1xml = sys.argv[1]
    if len(sys.argv)>2: hltxml = sys.argv[2]

    menu = createMenu(l1xml, hltxml)
    menu.printIt()

