#!/usr/bin/env python
#---------------------------------------------------------------------------
# Parses the output from iLumiCalc.exe and dump the integrated luminosity
# for each run into a simple table format.
#
# Run | N_LB | Lumi(pb-1)
#---------------------------------------------------------------------------

import os, sys
import re
import optparse

def parseLumiCalc(fin):
    rundata = {}
    re_run = re.compile('Beginning calculation for Trigger ([\w_]+) Run (\d+) LB \[(\d+)-(\d+)\]')
    re_header = re.compile('Run    L1-Acc    L2-Acc    L3-Acc  LiveTime  IntL')
    # Lumi data (run, L1acc, L2acc, EFacc, LiveTime, IntL(rec), IntL(del) )
    re_data = re.compile('([\d.e+-]+)\s+([\d.e+-]+)')
    #
    expect_run = True
    expect_header = False
    expect_data = False
    trigger, run, nlb = '', 0, 0
    #
    for line in fin.readlines():
        if len(line)>0: line = line[:-1]
        #print 'Check line(%d,%d,%d): %s' % \
        #      (expect_run, expect_header, expect_data, line)
        if expect_run:
            mg = re_run.search(line)
            if mg:
                #print 'Matched to begin run!'
                #print re_run
                #print dir(re_run)
                (trigger, run, lb0, lb1) = mg.groups()
                run, lb0, lb1 = int(run), int(lb0), int(lb1)
                if run in rundata.keys():
                    rundata[run][0] += (lb1-lb0+1)
                else:
                    # Run: [ nLB, Lumi(rec) ]
                    rundata[run] = [ lb1-lb0+1, 0.0, 0.0]
                expect_run = False
                expect_header = True
        elif expect_header:
            mg = re_header.search(line)
            if mg:
                #print 'Matched to header!'
                expect_header = False
                expect_data = True
        elif expect_data:
            n = len('--- LumiCalculator      :      Total    L1-Acc    L2-Acc    L3-Acc  LiveTime  ')
            if len(line)<n:
                print 'Unexpected format for the lumi data'
            #print 'Extract lumi data!'
            mg = re_data.search(line[n:])
            lumi_rec, lumi_del = 0.0, 0.0
            if mg:
                lumi_rec = float(mg.group(1))
                lumi_del = float(mg.group(2))
                #print mg.groups()
            rundata[run][1] += lumi_rec * 1E-6 # ub-1 --> pb-1
            rundata[run][2] += lumi_del * 1E-6 # ub-1 --> pb-1
            expect_data = False
            expect_run = True
    return rundata

def dumpLumiTable(rundata, fout):
    runs = rundata.keys()
    runs.sort()
    fout.write('# Run   N(LB)  Lumi(rec)  Lumi(del) (pb-1)\n')
    for r in runs:
        data = rundata[r]
        fout.write('%6d %4d %10.5f %10.5f\n' % (r, data[0], data[1], data[2]) )
    pass

def parse_args():
    op = optparse.OptionParser()
    op.add_option('-i', '--ilumicalc-output', dest='ilumicalc_output',
                  action='store', default='lumi.txt',
                  help='Output of iLumiCalc.exe')
    op.add_option('-o', '--output-file', dest='output_file',
                  action='store', default='LumiTable.txt',
                  help='Output file name with a table of luminosity for runs')
    return op.parse_args()

if __name__ == '__main__':
    options, args = parse_args()
    lumi_file = options.ilumicalc_output
    output_file = options.output_file

    fin, fout = None, None
    if os.path.exists(lumi_file):
        fin = open(lumi_file, 'r')
    else:
        sys.exit(1)
    fout = open(output_file, 'w')
    rundata = parseLumiCalc(fin)
    dumpLumiTable(rundata, fout)
    fin.close()
    fout.close()
    total = sum(map(lambda x: x[1], rundata.values() ) )
    print 'Table of luminosity for each run -> %s' % output_file
    print 'Total recorded luminosity = %10.5f (pb-1)' % total
