#!/usr/bin/env zsh

jobid_file='ganga_jobid'

jobid=''
if [[ -e $jobid_file ]]; then
    jobid=`cat $jobid_file`
else
    echo "File 'ganga_jobid' not found"
    exit 1
fi

tmp_resubmit='tmp_resubmit.py'
rm -f $tmp_resubmit;
cat <<EOF > $tmp_resubmit
jobid=${jobid}
if jobid not in jobs.ids():
  print 'Jobid %d not in GANGA (possible IDs are %s)' % (jobid,str(jobs.ids()))
else:
  for subjob in jobs[$jobid].subjobs:
    if subjob.status == 'failed':
      subjob.resubmit()
EOF

ganga $tmp_resubmit

