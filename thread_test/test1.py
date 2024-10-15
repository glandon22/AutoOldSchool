# 2134,9305,0
import time
from datetime import datetime

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
'''def pre():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'3372,11492,0'})
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_tiles('3372,11492,0') and qh.get_player_world_location('x') == 3374 and qh.get_player_world_location('y') == 11491:
        osrs.move.fast_click_v2(qh.get_tiles('3372,11492,0'))'''
'''osrs.move.interact_with_object_v3(
        44776,
        custom_exit_function=lambda start: (datetime.now() - start).total_seconds() > 9,
        custom_exit_function_arg=datetime.now(),
    #pre_interact=pre
    )'''

pyautogui.moveTo(516, 953)