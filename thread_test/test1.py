# 2134,9305,0
import time

import pyautogui
import osrs

qh = osrs.queryHelper.QueryHelper()
qh.set_npcs_by_name(['sir vyvin'])
qh.query_backend()
print(qh.get_npcs_by_name())