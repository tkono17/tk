#!/usr/bin/env python
import sys
import os
import xml.dom.minidom
from ROOT import TH1F, TFile

ConfigSource1 = [
    'LVL1config_lumi1E31_13.0.40.xml', 
    'HLTconfig_lumi1E31_13.0.40.xml', 
    ]
ConfigSource2 = [
    'LVL1config_lumi1E32_13.0.40.xml', 
    'HLTconfig_lumi1E32_13.0.40.xml', 
    ]

#---------------------------------------------------------------------------

class L1Item:
    def __init__(self, id=-1, name='', prescale=1):
        self.id = id
        self.name = name
        self.prescale = prescale
    def __eq__(self, x):
        if x.id == self.id and \
           x.name == self.name and \
           x.prescale == self.prescale:
            return True
        else:
            return False
    def __expr__(self):
        s = '%4d %-30s %8d' % (self.id, self.name, self.prescale)
        return s
    def __str__(self):
        s = '%4d %-30s %8d' % (self.id, self.name, self.prescale)
        return s
    def write(self, out):
        out.write('%s\n' % str(self))

class HLTChain:
    def __init__(self, id, level, name, lower_chain, ps, pt):
        self.id = id
        self.level = level
        self.name = name
        self.lower_chain = lower_chain
        self.prescale = ps
        self.pass_through = pt
        self.ps_total = ps
        self.pt_total = pt
    def update(self, lower_config):
        if self.lower_chain != '':
            lc = lower_config.findItem(self.lower_chain)
            if self.level == 'EF':
                self.ps_total = self.prescale * lc.ps_total
                if self.pass_through != 0:
                    self.pt_total = self.pass_through * lc.pt_total
                else:
                    self.pt_total = lc.pt_total
            elif self.level == 'L2':
                self.ps_total = self.prescale * lc.prescale
    def __eq__(self, x):
        if x.id == self.id and \
           x.name == self.name and \
           x.prescale == self.prescale and \
           x.pass_through == self.pass_through:
            return true
        else:
            return false
    def __expr__(self):
        s = '%4d %-30s %8d %8d %8d %8d' % \
            (self.id, self.name, self.prescale, self.pass_through, self.ps_total, self.pt_total)
        return s
    def __str__(self):
        s = '%4d %-30s %8d %8d %8d %8d' % \
            (self.id, self.name, self.prescale, self.pass_through, self.ps_total, self.pt_total)
        return s
    def write(self, out):
        out.write('%s\n' % str(self))

class ItemPair:
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2
        pass
    def isSame(self):
        if self.item1 == self.item2:
            return True
        else:
            return False
    def isDiff(self):
        return not self.isSame()
    def write(self, out):
        out.write('L1_common1: %s\n' % self.item1)
        out.write('L1_common2: %s\n' % self.item2)

def compareConfig(config1, config2):
    items_common = []
    items_only1 = []
    items_only2 = []
    items1 = config1.allItems()
    items2 = config2.allItems()
    for item in items1:
        found_it = False
        for i2 in items2:
            if item.name == i2.name:
                items_common.append(ItemPair(item, i2))
                found_it = True
                break
        if not found_it:
            items_only1.append(item)
    for item in items2:
        found_it = False
        for i2 in items1:
            if i2.name == item.name:
                found_it = True
                break
        if not found_it:
            items_only2.append(item)
    return (items_common, items_only1, items_only2)    

class TrigConfig:
    def __init__(self, its):
        self.items = its
        pass
    def readXML(self, xmlfile):
        pass
    def allItems(self):
        return self.items
    def setItems(self, items):
        self.items = items
    def findItem(self, name):
        items = self.allItems()
        for i in items:
            if i.name == name:
                return i
        return None
    def write(self, tag, out):
        out.write('%s\n' % tag)
        for i in self.allItems():
            i.write(out)
    def fillPrescales(self, h):
        for i in self.allItems():
            h.GetXaxis().SetBinLabel(i.id+1, i.name)
            h.SetBinContent(i.id+1, i.prescale)

class L1Config(TrigConfig):
    def __init__(self, its):
        TrigConfig.__init__(self, its)
        pass
    def prescaleElement(self, pss, id):
        value = 1
        for ps in pss:
            nodes = ps.childNodes
            if id == int(ps.getAttribute('ctpid')):
                for n in nodes:
                    if n.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                        value = int(n.nodeValue)
        return value
    def readXML(self, xmlfile):
        if os.path.exists(xmlfile):
            print 'Reading L1 config from %s' % xmlfile
            doc = xml.dom.minidom.parse(xmlfile)
            menu = doc.getElementsByTagName('TriggerMenu')
            pss0 = doc.getElementsByTagName('PrescaleSet')
            if len(pss0) != 1:
                print 'Warning: cannot PrescaleSet tag in file %s', xmlfile
            pss = pss0[0].getElementsByTagName('Prescale')
            if len(menu)==1:
                items = menu[0].getElementsByTagName('TriggerItem')
                for i in items:
                    id = int(i.getAttribute('ctpid'))
                    name = i.getAttribute('name')
                    ps = self.prescaleElement(pss, id)
                    # print 'id=%d, name=%s, ps=%d' % (id, name, ps)
                    if not self.findItem(name):
                        # print 'adding item ', name
                        self.items.append(L1Item(id, name, ps))
        else:
            print 'Warning: cannot find L1 XML file: %s', xmlfile
        pass
    def allItems(self):
        return self.items
    def compare(config1, config2):
        (items, items1, items2) = compareConfig(config1, config2)
        return (L1Config(items), L1Config(items1), L1Config(items2))
    

class HLTConfig(TrigConfig):
    def __init__(self, level, chains):
        TrigConfig.__init__(self, chains)
        self.level = level
        pass
    def readXML(self, xmlfile):
        if os.path.exists(xmlfile):
            print 'Reading HLT config from %s' % xmlfile
            doc = xml.dom.minidom.parse(xmlfile)
            menu = doc.getElementsByTagName('CHAIN_LIST')
            if len(menu)==1:
                items = menu[0].getElementsByTagName('CHAIN')
                for i in items:
                    level = i.getAttribute('level')
                    if level != self.level: continue
                    id = int(i.getAttribute('chain_counter'))
                    name = i.getAttribute('chain_name')
                    lc = i.getAttribute('lower_chain_name')
                    ps = int(i.getAttribute('prescale'))
                    pt = int(i.getAttribute('pass_through'))
                    # print 'id=%d, name=%s, ps=%d, pt=%d' % (id, name, lc, ps, pt)
                    if not self.findItem(name):
                        # print 'adding item ', name
                        self.items.append(HLTChain(id, level, name, lc, ps, pt))
            pass
        else:
            print 'Warning: cannot find L1 XML file: %s', xmlfile
    def allItems(self):
        return self.items
    def compare(config1, config2):
        (items, items1, items2) = compareConfig(config1, config2)
        return (HLTConfig(config1.level, items),
                HLTConfig(config1.level, items1),
                HLTConfig(config1.level, items2))
    def update(self, lower_config):
        for i in self.allItems():
            i.update(lower_config)
    def fillPassThrough(self, h):
        for i in self.allItems():
            h.GetXaxis().SetBinLabel(i.id+1, i.name)
            h.SetBinContent(i.id+1, i.pass_through)
    def fillTotalPS(self, h):
        for i in self.allItems():
            h.GetXaxis().SetBinLabel(i.id+1, i.name)
            h.SetBinContent(i.id+1, i.ps_total)
    def fillTotalPT(self, h):
        for i in self.allItems():
            h.GetXaxis().SetBinLabel(i.id+1, i.name)
            h.SetBinContent(i.id+1, i.pt_total)

class CompResult:
    def __init__(self, name):
        self.common_file = name + '_common.dat'
        self.only1_file = name + '_only1.dat'
        self.only2_file = name + '_only2.dat'
        self.CommonFile = None
        self.Only1File = None
        self.Only2File = None
        self.openFiles()
    def openFiles(self):
        self.closeFiles()
        self.CommonFile = open(self.common_file, 'w')
        self.Only1File = open(self.only1_file, 'w')
        self.Only2File = open(self.only2_file, 'w')
    def closeFiles(self):
        self.closeFile(self.CommonFile)
        self.closeFile(self.Only1File)
        self.closeFile(self.Only2File)
    def closeFile(self, f):
        if f!=None:
            f.close()
            f = None
    def commonFile(self):
        return self.CommonFile
    def only1File(self):
        return self.Only1File
    def only2File(self):
        return self.Only2File
    
#-----------------------------------------------------------------------
# Start of the program
#-----------------------------------------------------------------------
L1config1 = L1Config([])
L2config1 = HLTConfig('L2', [])
EFconfig1 = HLTConfig('EF', [])

# Read configuration from XML files
print 'Read config1'
L1config1.readXML(ConfigSource1[0])
L2config1.readXML(ConfigSource1[1])
EFconfig1.readXML(ConfigSource1[1])
L2config1.update(L1config1)
EFconfig1.update(L2config1)


print 'Read config2'
L1config2 = L1Config([])
L2config2 = HLTConfig('L2', [])
EFconfig2 = HLTConfig('EF', [])

L1config2.readXML(ConfigSource2[0])
L2config2.readXML(ConfigSource2[1])
EFconfig2.readXML(ConfigSource2[1])
L2config2.update(L1config2)
EFconfig2.update(L2config2)

## L1config1.setItems([
##     L1Item(0, 'item0'), 
##     L1Item(1, 'item1', 2), 
##     L1Item(2, 'item2'),
##     ])
## L1config2.setItems([
##     L1Item(0, 'item0'), 
##     L1Item(1, 'item1', 32), 
##     L1Item(3, 'item3'),
##     L1Item(4, 'item4'),
##     ])

L1result = CompResult('L1')
L2result = CompResult('L2')
EFresult = CompResult('EF')

#L1config1.write('config1', sys.stdout)
#L2config1.write('config1', sys.stdout)
#EFconfig1.write('config1', sys.stdout)
#L1config2.write('config2', sys.stdout)
#L2config2.write('config2', sys.stdout)
#EFconfig2.write('config2', sys.stdout)

# Check L1 config
(cfg_common, cfg_only1, cfg_only2) = L1Config.compare(L1config1, L1config2)
cfg_common.write('# Common\n#-----------', L1result.commonFile())
cfg_only1.write('# Only in menu1\n#-----------', L1result.only1File())
cfg_only2.write('# Only in menu2\n#-----------', L1result.only2File())
# Check L2 config
(cfg_common, cfg_only1, cfg_only2) = HLTConfig.compare(L2config1, L2config2)
cfg_common.write('# Common\n#-----------', L2result.commonFile())
cfg_only1.write('# Only in menu1\n#-----------', L2result.only1File())
cfg_only2.write('# Only in menu2\n#-----------', L2result.only2File())
# Check EF config
(cfg_common, cfg_only1, cfg_only2) = HLTConfig.compare(EFconfig1, EFconfig2)
cfg_common.write('# Common\n#-----------', EFresult.commonFile())
cfg_only1.write('# Only in menu1\n#-----------', EFresult.only1File())
cfg_only2.write('# Only in menu2\n#-----------', EFresult.only2File())


L1result.closeFiles()
L2result.closeFiles()
EFresult.closeFiles()

f = TFile('f.root', 'RECREATE')

h_l1ps_1 = TH1F('h_l1ps_1', '', 256, 0, 256)
h_l1ps_2 = TH1F('h_l1ps_2', '', 256, 0, 256)
h_l2ps_1 = TH1F('h_l2ps_1', '', 1024, 0, 1024)
h_l2ps_2 = TH1F('h_l2ps_2', '', 1024, 0, 1024)
h_l2pt_1 = TH1F('h_l2pt_1', '', 1024, 0, 1024)
h_l2pt_2 = TH1F('h_l2pt_2', '', 1024, 0, 1024)

h_efps_1 = TH1F('h_efps_1', '', 1024, 0, 1024)
h_efps_2 = TH1F('h_efps_2', '', 1024, 0, 1024)
h_efpt_1 = TH1F('h_efpt_1', '', 1024, 0, 1024)
h_efpt_2 = TH1F('h_efpt_2', '', 1024, 0, 1024)
h_efps_total_1 = TH1F('h_efps_total_1', '', 1024, 0, 1024)
h_efps_total_2 = TH1F('h_efps_total_2', '', 1024, 0, 1024)
h_efpt_total_1 = TH1F('h_efpt_total_1', '', 1024, 0, 1024)
h_efpt_total_2 = TH1F('h_efpt_total_2', '', 1024, 0, 1024)

hists = [
    h_l1ps_1, h_l1ps_2,
    h_l2ps_1, h_l2ps_2, h_l2pt_1, h_l2pt_2, 
    h_efps_1, h_efps_2, h_efpt_1, h_efpt_2, 
    h_efps_total_1, h_efps_total_2, h_efpt_total_1, h_efpt_total_2, 
    ]

L1config1.fillPrescales(h_l1ps_1)
L1config2.fillPrescales(h_l1ps_2)
L2config1.fillPrescales(h_l2ps_1)
L2config2.fillPrescales(h_l2ps_2)
L2config1.fillPassThrough(h_l2pt_1)
L2config2.fillPassThrough(h_l2pt_2)

EFconfig1.fillPrescales(h_efps_1)
EFconfig2.fillPrescales(h_efps_2)
EFconfig1.fillPassThrough(h_efpt_1)
EFconfig2.fillPassThrough(h_efpt_2)
EFconfig1.fillTotalPS(h_efps_total_1)
EFconfig2.fillTotalPS(h_efps_total_2)
EFconfig1.fillTotalPT(h_efpt_total_1)
EFconfig2.fillTotalPT(h_efpt_total_2)

for a in hists: a.Write()
f.Write()
f.Close()

