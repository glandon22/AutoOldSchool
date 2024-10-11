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
qh = osrs.queryHelper.QueryHelper()
qh.set_objects_v2('game', {21280})
qh.set_player_world_location()
while True:
    qh.query_backend()
    print('-------------------')
    obs = qh.get_objects_v2('game')
    obs = osrs.util.find_closest_target_on_screen(list(
        sorted(
            obs,
            key=lambda x: x['dist']
        )
    ))
    print(obs)

#pyautogui.moveTo(858, 591)