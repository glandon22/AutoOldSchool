# 2134,9305,0
import time

import pyautogui
import osrs
a = set()
qh = osrs.queryHelper.QueryHelper()
qh.set_orientation()
while True:
    qh.query_backend()
    a.add(qh.get_orientation())
    print(sorted(a, reverse=True))