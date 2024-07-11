# 2134,9305,0
import time

import pyautogui
import osrs

import osrs
qh = osrs.queryHelper.QueryHelper()
qh.set_equipment()
qh.query_backend()
print(qh.get_equipment(osrs.item_ids.ItemIDs.EARTH_TIARA.value + 1))