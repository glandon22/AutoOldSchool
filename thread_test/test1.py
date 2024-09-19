# 2134,9305,0
import time

import pyautogui
import osrs
time.sleep(0.5)
qh = osrs.queryHelper.QueryHelper()
qh.set_inventory()
qh.query_backend()
osrs.inv.power_drop_v2(qh.get_inventory(), [osrs.item_ids.OAK_LOGS])
