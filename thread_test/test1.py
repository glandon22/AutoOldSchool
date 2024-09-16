# 2134,9305,0
import time

import pyautogui
import osrs
qh = osrs.queryHelper.QueryHelper()
qh.set_player_world_location()
while True:
    qh.query_backend()
    print(qh.get_player_world_location())