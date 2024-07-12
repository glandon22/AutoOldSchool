# 2134,9305,0
import time

import pyautogui
import osrs

qh = osrs.queryHelper.QueryHelper()
qh.set_active_prayers()
qh.query_backend()
print(qh.get_active_prayers())