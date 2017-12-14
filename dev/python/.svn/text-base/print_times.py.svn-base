#!/usr/bin/env python

import sched, time
import datetime

def print_time():
    print "From print_time", datetime.datetime.now()

s = sched.scheduler(time.time, time.sleep)

def print_some_times():
    print datetime.datetime.now()
    s.enter(5, 1, print_time, ())
    s.enter(3600, 1, print_time, ())
    s.run()
    print datetime.datetime.now()

if __name__=='__main__':
    print_some_times()

