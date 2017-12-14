#!/usr/bin/env python

import xml.dom.minidom
import os
import commands
import sys

trig_config='lumi1E31'

def usage():
    print 'Usage: %s <TriggerMenuName>' % (sys.argv[0])
    print '------'
    print 'Example: %s lumi1E31'

if len(sys.argv)>1:
    trig_config = sys.argv[1]
else:
    usage()
    sys.exit(1)

# config_dir='/space2/tkohno/athena/13.0.X/Trigger/TriggerCommon/TriggerMenuXML/data/'
# config_dir='/space2/tkohno/work/rel13_dev/testNewConfig'
config_dir='/space2/tkohno/athena/13.0.X/InstallArea/XML/TriggerMenuXML/'
l1config_file = 'LVL1config_%s_13.0.40.2.xml' % trig_config
hltconfig_file = 'HLTconfig_%s_13.0.40.2.xml' % trig_config
merged_file = 'TriggerConfig_%s_13.0.40.2.xml' % trig_config
output_file = '~/WWW/TrigConf_%s_13.0.40.2.xml' % trig_config
xsl_file = 'tm.xsl'


def mergeXmlFiles():
    l1_fname = os.path.join(config_dir, l1config_file)
    hlt_fname = os.path.join(config_dir, hltconfig_file)
    print 'l1 file: ', l1_fname
    print 'HLT file: ', hlt_fname
    l1doc = xml.dom.minidom.parse(l1_fname)
    hltdoc = xml.dom.minidom.parse(hlt_fname)

    merged_doc = xml.dom.minidom.Document()
    top_node = merged_doc.createElement('TriggerConfig')
    merged_doc.appendChild(top_node)
    top_node.setAttribute('name', merged_file.replace('.xml', ''))
    for e in l1doc.getElementsByTagName('LVL1Config'):
        top_node.appendChild(e)
    for e in hltdoc.getElementsByTagName('HLT_MENU'):
        top_node.appendChild(e)
    
    fout = open(merged_file, 'w')
    fout.write(merged_doc.toprettyxml('', '  '))
    fout.close()

if not os.path.exists(merged_file): mergeXmlFiles()

cmd = 'proc_xslt.py -s %s -x %s -o %s' % (xsl_file, merged_file, output_file)
print cmd
(status, output) = commands.getstatusoutput(cmd)
print output
if status != 0:
    print 'Error while calling proc_xslt.py'

