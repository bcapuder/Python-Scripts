# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 18:20:33 2014

@author: User
"""

from apscheduler.scheduler import Scheduler
import jailbase


# Start the scheduler
sched = Scheduler()
@sched.interval_schedule(minutes=360)
def my_job():
    jailbase.jailbasescrape()


sched.start()
while True:
    pass
