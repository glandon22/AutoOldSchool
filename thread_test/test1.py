# 2134,9305,0
import time

import pyautogui
import osrs
osrs.bank.ge_handler_v2([
        {
            'id': osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value, 'sell': True,
            'quantity': '6500', 'id_override': 'varrock teleport'
        },
        {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 1},
        {'id': osrs.item_ids.ItemIDs.LAW_RUNE.value, 'quantity': 1},
        {'id': osrs.item_ids.ItemIDs.SOFT_CLAY.value, 'quantity': 1},
        {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': 1}
    ])