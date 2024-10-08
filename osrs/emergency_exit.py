"""
This script always runs and is an emergency utility to ensure that I never bot for more than a specified time,
about 1 hour.
"""
import time

import psutil

import osrs.dev as dev
import osrs.queryHelper as qh
from threading import Thread


def check_session_time():
    qh1 = qh.QueryHelper()
    qh1.set_widgets({'162,33'})
    while True:
        qh1.query_backend()
        if qh1.get_widgets('162,33') and qh1.get_widgets('162,33')['text']:
            parsed_time = qh1.get_widgets('162,33')['text'].split(':')
            if int(parsed_time[0]) >= 1 and int(parsed_time[1]) > 10:
                dev.logger.critical('Script is malfunctioning, ran for over 1 hour. Emergency exit.')
                for process in psutil.process_iter():
                    cmdline = process.cmdline()
                    if len(cmdline) >= 2 and 'AutoOldSchool' in cmdline[0]:
                        process.kill()
        time.sleep(60)


t = Thread(target=check_session_time)
t.start()
