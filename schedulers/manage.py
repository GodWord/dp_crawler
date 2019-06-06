# -*- coding:utf-8 -*-
__author__ = 'zhoujifeng'
__date__ = '2019/3/12 18:44'

from apscheduler.schedulers.blocking import BlockingScheduler



def start_schedulers():
    sched = BlockingScheduler()
    # TODO : add your job here

    sched.start()
