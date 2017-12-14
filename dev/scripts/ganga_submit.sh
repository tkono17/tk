#!/usr/bin/env zsh

function usage() {
    echo "Usage: $0 <ganga_script>"
}

job_config=""
package_path="TkAthena/AnalysisJobs/ESDAnalysis"

if [[ $#@ -eq 0 ]]; then
    usage;
    exit 0
else
    job_config=$1;
fi

if [[ $#@ -ge 2 ]]; then
    package_path=$2;
fi
package_abspath=$TestArea/${package_path};

echo "Input parameters"
echo "job_config: $job_config"
echo "package_abspath: $package_abspath"

if [[ ! -e $job_config ]]; then
    echo "GANGA script $job_config does not exist";
    exit -1
fi

ganga_out=`pwd`/ganga_sub.out
ganga_err=`pwd`/ganga_sub.err

job_config_abspath=`pwd`/${job_config}
if [[ -d ${package_abspath} && -d ${package_abspath}/cmt ]]; then
    cd $package_abspath/cmt;
    ganga $job_config_abspath 1>$ganga_out 2>$ganga_err;
    cd -;
else
    echo "No directory ${package_abspath}/cmt found";
    exit -1
fi


python -c "
import os, re
fname='${ganga_err}'
dir=os.path.dirname(fname)
if os.path.exists(fname):
  f = open(fname, 'r')
  for line in f.readlines():
    mg = re.search('submitting job (\d+)[^.\d]', line)
    if mg:
      fname_out='ganga_jobid'
      if len(dir)>0: fname_out = dir+os.sep+fname_out
      fout = open(fname_out, 'w')
      fout.write(mg.group(1)+'\n')
      fout.close()
else:
  print 'GANGA Job ID could not be found'
"
