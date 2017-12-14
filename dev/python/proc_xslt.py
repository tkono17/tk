#!/usr/bin/env python
#------------------------------------------------------------------------
# proc_xslt.py
# 
#------------------------------------------------------------------------
import os
import sys
import xml.dom.minidom
import getopt

#------------------------------------------------------------------------
def usage():
    print 'Usage: proc_xslt.py [options]'
    print 'Options: -s ..... XSL file'
    print '         -x ..... XML file to transform'
    print '         -o ..... Output XML file'
    
def proc_xslt(xsl_file, xml_file):
    command = 'xsltproc %s %s' % (xsl_file, xml_file)
    f = os.popen(command, 'r')
    return f

def format_xml(f, out_file=''):
    fout = open(out_file, 'w')
    fout.write(f.read())
    fout.close()
    return 0
##     indent = '  '
##     doc = xml.dom.minidom.parse(f)
##     if out_file!='':
##         f = open(out_file, 'w')
##         f.write(doc.toprettyxml(indent))
##     else:
##         print doc.toprettyxml(indent)
##     return 0

#------------------------------------------------------------------------
if __name__=='__main__':
    xsl_file = ''
    xml_file = ''
    out_file = ''
    args = sys.argv[1:]
    (optvals, args) = getopt.getopt(args, 'hs:x:o:')
    if len(args) > 0:
        usage();
        sys.exit(0)
    else:
        for o, v in optvals:
            if o=='-h':
                usage()
                sys.exit(0)
            elif o=='-s':
                xsl_file = v
            elif o=='-x':
                xml_file = v
            elif o=='-o':
                out_file = v
        if xsl_file=='' or xml_file=='':
            print 'XSL and XML files must be provided'
            usage()
            sys.exit(0)
        f = proc_xslt(xsl_file, xml_file)
        status = format_xml(f, out_file)
        f.close()
        if status!=0:
            print 'Error while XSLT'
            
