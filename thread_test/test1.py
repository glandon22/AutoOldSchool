# 2134,9305,0
import time

import pyautogui
import osrs
'''time.sleep(0.5)
qh = osrs.queryHelper.QueryHelper()
qh.set_widgets({'161,96', '161,97'})
qh.query_backend()
print(osrs.util.combine_objects(qh.get_widgets()))'''
'''def exx():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 3145 <= qh.get_player_world_location('x') <= 3180:
        osrs.keeb.press_key('esc')
        return True


def pre():
    #osrs.keeb.press_key('f6')
    print('test')

osrs.move.interact_with_widget_v3(
    osrs.widget_ids.varrock_tele_widget_id,
    right_click_option='Grand Exchange',
    custom_exit_function=exx,
    pre_interact=pre
)'''
'''qh = osrs.queryHelper.QueryHelper()
qh.set_destination_tile()
qh.set_player_world_location()
qh.set_projectiles_v2()
while True:
    qh.query_backend()
    print('-------------------')
    print(qh.get_projectiles_v2())
    print(qh.get_player_world_location())
    print('-------------------')
'''
#osrs.player.equip_item([osrs.item_ids.DIAMOND_DRAGON_BOLTS_E])
qh = osrs.queryHelper.QueryHelper()
qh.set_objects_v2('game', {31421})
while True:
    qh.query_backend()
    print(qh.get_objects_v2('game'))