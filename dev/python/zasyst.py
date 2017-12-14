#!/usr/bin/python2.2
#
import sys
import string
import os

program_name = 'echo'
program_type = 'xsec'
output_dir = '/s/'
inputfile_data = 'files/data1_all.txt'
inputfile_herwig = 'files/herwig_cphpj.txt'
inputfile_pythia = 'files/pythia_cphpj.txt'
inputdir_data = 'jet1/data'
inputdir_herwig = 'jet1/herwig'
inputdir_pythia = 'jet1/pythia'

def mk_command(pname, option, infile, outdir, outfile, indir):
    command = \
            "nice -10 %s %s %s %s/%s %s" % \
            (pname, option, infile, outdir, outfile, indir)
    return command

def run_syst1():
    out_fname = "%s_syst1.root" % program_type
    command = mk_command(program_name, '-dr --syst=1', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=1', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    
def run_syst2():
    out_fname = "%s_syst2a.root" % program_type
    command = mk_command(program_name, '-dr --syst=2a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=2a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst2b.root" % program_type
    command = mk_command(program_name, '-dr --syst=2b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=2b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst3():
    out_fname = "%s_syst3a.root" % program_type
    command = mk_command(program_name, '-dr --syst=3a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=3a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst3b.root" % program_type
    command = mk_command(program_name, '-dr --syst=3b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=3b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst4():
    out_fname = "%s_syst4a.root" % program_type
    command = mk_command(program_name, '-dr --syst=4a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=4a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst4b.root" % program_type
    command = mk_command(program_name, '-dr --syst=4b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=4b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst5():
    out_fname = "%s_syst5a.root" % program_type
    command = mk_command(program_name, '-dr --syst=5a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=5a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst5b.root" % program_type
    command = mk_command(program_name, '-dr --syst=5b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=5b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst6():
    out_fname = "%s_syst6a.root" % program_type
    command = mk_command(program_name, '-dr --syst=6a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=6a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst6b.root" % program_type
    command = mk_command(program_name, '-dr --syst=6b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=6b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst7():
    out_fname = "%s_syst7a.root" % program_type
    command = mk_command(program_name, '-dr --syst=7a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=7a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst7b.root" % program_type
    command = mk_command(program_name, '-dr --syst=7b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=7b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst10():
    print 'No need to run with another setting, just use PYTHIA.'
    
def run_syst11():
    out_fname = "%s_syst11a.root" % program_type
    command = mk_command(program_name, '-dr --syst=11a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=11a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst11b.root" % program_type
    command = mk_command(program_name, '-dr --syst=11b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=11b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst12():
    out_fname = "%s_syst12a.root" % program_type
    command = mk_command(program_name, '-dr --syst=12a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=12a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst12b.root" % program_type
    command = mk_command(program_name, '-dr --syst=12b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=12b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst13():
    out_fname = "%s_syst13a.root" % program_type
    command = mk_command(program_name, '-dr --syst=13a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=13a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst13b.root" % program_type
    command = mk_command(program_name, '-dr --syst=13b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=13b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst14():
    out_fname = "%s_syst14a.root" % program_type
    command = mk_command(program_name, '-dr --syst=14a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=14a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst14b.root" % program_type
    command = mk_command(program_name, '-dr --syst=14b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=14b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst15():
    out_fname = "%s_syst15a.root" % program_type
    command = mk_command(program_name, '-dr --syst=15a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=15a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst15b.root" % program_type
    command = mk_command(program_name, '-dr --syst=15b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=15b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst16():
    out_fname = "%s_syst16a.root" % program_type
    command = mk_command(program_name, '-dr --syst=16a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=16a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst16b.root" % program_type
    command = mk_command(program_name, '-dr --syst=16b', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=16b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst17():
    out_fname = "%s_syst17a.root" % program_type
    command = mk_command(program_name, '-dr --syst=17a', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=17a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst18():
    out_fname = "%s_syst18a.root" % program_type
    command = mk_command(program_name, '-dr --syst=18a', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)
    out_fname = "%s_syst18b.root" % program_type
    command = mk_command(program_name, '-m  --syst=18b', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst31():
    out_fname = "%s_syst31.root" % program_type
    command = mk_command(program_name, '-dr --syst=31', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=31', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)

def run_syst32():
    out_fname = "%s_syst32.root" % program_type
    command = mk_command(program_name, '-dr --syst=32', inputfile_data, \
                         output_dir, out_fname, inputdir_data)
    os.system(command)
    command = mk_command(program_name, '-m  --syst=32', inputfile_herwig, \
                         output_dir, out_fname, inputdir_herwig)
    os.system(command)



syst_defined = (
    1,  # Et correction
    2,  # Zvtx
    3,  # pt(pis)
    4,  # pt(pi)
    5,  # pt(K)
    6,  # eta(track)
    7,  # D* signal
    10, # PYTHIA
    11, # Jet energy scale
    12, # Et(jet) cut
    13, # W cut
    14, # eta(jet) cut
    15, # pt(D*) cut
    16, # eta(D*) cut
    17, # b fraction
    18, # FLT efficiency
    31, # eta(jet) reweighting
    32  # pt(D*)/Et(jet) reweighting
    )

syst_defined2 = {
    '1': ['1'], 
    '2': ['2a', '2b'],
    '3': ['3a', '3b'],
    '4': ['4a', '4b'],
    '5': ['5a', '5b'],
    '6': ['6a', '6b'],
    '7': ['7a', '7b'],
    '10': ['10'],
    '11': ['11a', '11b'],
    '12': ['12a', '12b'],
    '13': ['13a', '13b'],
    '14': ['14a', '14b'],
    '15': ['15a', '15b'],
    '16': ['16a', '16b'],
    '17': ['17a'], 
    '18': ['18'], 
    '31': ['31'], 
    '32': ['32'],
    }
    
def run_syst(num):
    if num in syst_defined:
       if num == 1: run_syst1()
       if num == 2: run_syst2()
       if num == 3: run_syst3()
       if num == 4: run_syst4()
       if num == 5: run_syst5()
       if num == 6: run_syst6()
       if num == 7: run_syst7()
       if num == 10: run_syst10()
       if num == 11: run_syst11()
       if num == 12: run_syst12()
       if num == 13: run_syst13()
       if num == 14: run_syst14()
       if num == 15: run_syst15()
       if num == 16: run_syst16()
       if num == 17: run_syst17()
       if num == 18: run_syst18()
       if num == 31: run_syst31()
       if num == 32: run_syst32()

