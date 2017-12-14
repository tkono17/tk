#!/usr/bin/python2.2
#--------------------------------------------------------------------------
# Python module zcard
#---------------------
# Functions for dealing with control.cards of ZEUS analysis
#--------------------------------------------------------------------------
import os
import sys
import re
import string

def read_lumi_file(filename, exclude_runs=[]):
    re_run = re.compile(r'run')
    re_lumi = re.compile(r'lumi')
    myfile = open(filename, 'r')
    is_ready = 0
    runlist = []
    for line in myfile.readlines():
        if len(line)>0: line = line[:-1]
        run = '-1'
        nevents = '-1'
        lumi_cal = '0.0'
        lumi_spc = '0.0'
        gflt_no = '0'
        trigger = ''
        if is_ready==0:
            if re_run.search(line) and re_lumi.search(line):
#                print 'Start reading run/lumi after line', line
                is_ready = 1
        else:
            words = line.split()
            if len(words) < 3: continue
            del words[0]
            run = words[0]
            if not (run.isdigit() and string.atoi(run)>10000): continue
            if len(words) == 2:
                lumi_cal = words[1]
            elif len(words) == 3 or len(words)==4:
                lumi_cal = words[1]
                nevents = words[2]
            elif len(words) == 6:
                nevents = words[1]
                lumi_cal = words[2]
                lumi_spc = words[3]
                gflt_no = words[4]
                trigger = words[5]
            else:
                print 'How should I interprete this line', line
                continue
            if run.isdigit() and string.atoi(run)>0: # successfully read the line
                run = string.atoi(run)
                nevents = string.atoi(nevents)
                lumi_cal = string.atof(lumi_cal)
                lumi_spc = string.atof(lumi_spc)
                gflt_no = string.atoi(gflt_no)
                if not run in exclude_runs:
                    runlist.append(
                        (run, nevents, lumi_cal, lumi_spc, gflt_no, trigger))
                
    myfile.close()
    return runlist

def split_runlist(runlist, lumi_per_job=1000): # (nb-1)
    run_ranges = []
    a_runs = []
    a_lumi = 0.0
    a_event = 0
    for run in runlist:
        if (a_lumi+run[2]) > lumi_per_job:
            run_ranges.append( (a_runs, a_lumi, a_event))
            a_runs = []
            a_lumi = 0.0
            a_event = 0
        else:
            a_runs.append(run[0])
            a_lumi = a_lumi + run[2]
            a_event = a_event + run[1]
    return run_ranges

def mk_infi_card(runlist):
    myfile = open(outfile, 'w')
    myfile.close()

def mk_zes_cards(infile, suffix, lumi_per_job=1000): # (nb-1)
    # Read the lumi file and create 
    runlist = read_lumi_file(infile)
    jobs = split_runlist(runlist, lumi_per_job)
    i = 0
    for a in jobs:
        outfile = "control.cards.%s.%d" % (suffix, i)
        if len(a[0]) > 0:
            mk_zes_card(outfile, a[0][0], a[0][-1], a[1], a[2])
            i = i + 1

def mk_zes_card(outfile, first, last, total_lumi, total_event):
    myfile = open(outfile, 'w')
    myfile.write('C----------------------------------------\n')
    myfile.write('ZEUSIO-INFI ZeusEventStore\n')
    myfile.write('ZEUSIO-IOPT DRIVER=OBJY\n')
    line = "ZEUSIO-FirstRun  %d\n" % first
    myfile.write(line)
    line = "ZEUSIO-LastRun  %d\n" % last
    myfile.write(line)
    line = "C Total luminosity : %10.2f (nb-1)\n" % total_lumi
    myfile.write(line)
    line = "C Total number of events : %d\n" % total_event
    myfile.write(line)
    myfile.write('C----------------------------------------\n')
    myfile.close()

def combine_cards(base, sub):
    if os.path.exists('control.cards'):
        return
    if not os.path.exists(base):
        print 'Base cards not found: ', base
    if not os.path.exists(sub):
        print 'Sub cards not found: ', sub
    if not os.path.exists(base) or not os.path.exists(sub):
        return
    f1 = open(base, 'r')
    f2 = open(sub, 'r')
    fout = open('control.cards', 'w')
    re_insert = re.compile('^C ADD OTHER CARDS HERE')
    for a in f1.readlines():
        if re_insert.search(a):
            fout.write(a)
            for b in f2.readlines():
                fout.write(b)
        else:
            fout.write(a)
    f1.close()
    f2.close()
    fout.close()
    
def total_lumi(runlist, first=0, last=-1, exclude_runs=[]):
    lumi = 0.0
    for run in runlist:
        if run in exclude_runs: continue
        if first>last or (run[0]>=first and run[0]<=last):
            lumi = lumi + run[2]
    return lumi


if __name__ == '__main__':
    runlist = read_lumi_file(sys.argv[1])
    jobs = split_runlist(runlist)
    print 'number of jobs = ', len(jobs)
    


