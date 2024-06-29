# 2134,9305,0
import datetime

import pyautogui

import osrs
'''from combat import slayer_killer
pot_config = slayer_killer.PotConfig(super_str=True)
slayer_killer.main(
    'suqah',
    pot_config.asdict(), 35,
    attackable_area={'x_min': 2090, 'x_max': 2111, 'y_min': 3847, 'y_max': 3878},
)
'''

qh = osrs.queryHelper.QueryHelper()
qh.set_inventory()
qh.set_canvas()
qh.query_backend()
osrs.move.right_click_v6(qh.get_inventory(osrs.item_ids.ItemIDs.KARAMJA_GLOVES_3.value), 'Gem mine', qh.get_canvas(), in_inv=True)

'''

{'x': 570, 'y': 345, 'name': 'Marble gargoyle', 'id': 7407, 'dist': 10, 'graphic': -1, 'health': 16, 'scale': 60, 'x_coord': 3427, 'y_coord': 9943, 'compositionID': 7407, 'interacting': 'Lord Gazzy', 'cbLvl': 349}
PROJECTILE TO AVOID - 1453
'''