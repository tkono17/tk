#--------------------------------------------------------------------------
# A python script to be called by GANGA
#--------------------------------------------------------------------------

njobs = len(jobs)

print 'Number of jobs: %d' % njobs
for jid in jobs.ids():
    j = jobs[jid]
    print 'Job %d has %d sub jobs' % (jid, len(j.subjobs))
    print 'Job %d status : %s' % (jid, j.status)
    for (sjid, sj) in enumerate(j.subjobs):
        print 'Job %d-%d status: %s' % (jid, sjid, sj.status)

