# 2134,9305,0
import time

import pyautogui
import osrs

def wait_for_orbs_of_protection():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.RING_OF_DUELING4.value):
        return True

osrs.move.interact_with_object(
    osrs.item_ids.ItemIDs.RING_OF_DUELING4.value, 'x', 1, True,
    obj_type='ground_items', custom_exit_function=wait_for_orbs_of_protection)