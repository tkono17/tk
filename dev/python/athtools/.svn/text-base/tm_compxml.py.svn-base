#!/usr/bin/env python
#-----------------------------------------------------------
# tm_compxml.py
#-----------------------------------------------------------

import os,sys
import re
from tm_xml2list import createMenu

class MenuConf:
    def __init__(self, l1xml='', hltxml=''):
        self.l1xml = l1xml
        self.hltxml = hltxml

def checkMapping(conf1_list, conf2_list, slot):
    for y in conf1_list:
        # Find a matching item (by ID) in the other configuration
        y_in_2 = filter(lambda x: x[0]==y[0], conf2_list)
        if len(y_in_2) != 0:
            if len(y_in_2) != 1:
                print 'Found more than one %s with ID : ' % (slot, y[0])
            elif y[1] != y_in_2[0][1]:
                print 'Different %s assigined for ID=%d, %s and %s' % \
                      (slot, y[0], y[1], y_in_2[0][1])
            else:
                # print 'Found the same %s' % (slot)
                pass
        else:
            print 'No matching %s found %s' % (slot, y[1])
    
menuconf1 = MenuConf()
menuconf1.l1xml = '/afs/cern.ch/atlas/software/builds/nightlies/pcache/AtlasProduction/rel_2/InstallArea/XML/TriggerMenuXML/LVL1config_lumi1E32_13.0.40.2.xml'
menuconf1.hltxml = '/afs/cern.ch/atlas/software/builds/nightlies/pcache/AtlasProduction/rel_2/InstallArea/XML/TriggerMenuXML/HLTconfig_lumi1E32_13.0.40.2.xml'

menuconf2 = MenuConf()
menuconf2.l1xml = '/afs/cern.ch/user/t/tkohno/scratch0/test2/run/LVL1_FDR2_lumi1E32.xml'
menuconf2.hltxml = '/afs/cern.ch/user/t/tkohno/scratch0/test2/run/HLT_FDR2_lumi1E32.xml'


menuconf1.l1xml = 'MenuXML-newBjet/LVL1config_FDR2_lumi1E32_13.0.40.4.xml'
menuconf1.hltxml = 'MenuXML-newBjet/HLTconfig_FDR2_lumi1E32_13.0.40.4.xml'
menuconf2.l1xml = 'MenuXML/LVL1config_FDR2_lumi1E32_13.0.40.4.xml'
menuconf2.hltxml = 'MenuXML/HLTconfig_FDR2_lumi1E32_13.0.40.4.xml'

menuconf1.l1xml = 'MenuXML-newBjet/LVL1config_default_13.0.40.4.xml'
menuconf1.hltxml = 'MenuXML-newBjet/HLTconfig_default_13.0.40.4.xml'
menuconf2.l1xml = 'MenuXML/LVL1config_default_13.0.40.4.xml'
menuconf2.hltxml = 'MenuXML/HLTconfig_default_13.0.40.4.xml'

menuconf1.l1xml = 'data/LVL1config_lumi1E31_13.0.40.4.xml'
menuconf1.hltxml = 'data/HLTconfig_lumi1E31_13.0.40.4.xml'
menuconf2.l1xml = 'data/LVL1config_lumi1E32_13.0.40.4.xml'
menuconf2.hltxml = 'data/HLTconfig_lumi1E32_13.0.40.4.xml'

menuconf1.l1xml = 'LVL1config_lumi1E31_14.4.0.xml'
menuconf1.hltxml = 'HLTconfig_lumi1E31_14.4.0.xml'
menuconf2.l1xml = 'LVL1config_lumi1E31_14.5.0.3.xml'
menuconf2.hltxml = 'HLTconfig_lumi1E31_14.5.0.3.xml'

menu1 = createMenu(menuconf1.l1xml, menuconf1.hltxml)
menu2 = createMenu(menuconf2.l1xml, menuconf2.hltxml)


checkMapping(menu1.l1_items, menu2.l1_items, 'L1 item')
checkMapping(menu1.l2_chains, menu2.l2_chains, 'L2 chain')
checkMapping(menu1.ef_chains, menu2.ef_chains, 'EF chain')

