import datetime

import pyautogui

import osrs

hotspot = 15313
hotspot_off = 15314
lectern = 15420


def leave_house():
    house_portal_id = 4525
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2('game', {house_portal_id})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') < 5000:
            return
        elif qh.get_objects_v2('game', house_portal_id):
            osrs.move.fast_click(qh.get_objects_v2('game', house_portal_id)[0])


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main():
    rooms_holder = '212,1'
    study_widget = '212,25,1'
    chat_input_widget = '162,42'
    portal_id = 15478
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_npcs_by_name(['phials'])
    qh.set_chat_options()
    qh.set_objects_v2('game', {portal_id})
    qh.set_objects_v2('wall', {hotspot, hotspot_off})
    qh.set_widgets({chat_input_widget, rooms_holder, study_widget})
    last_portal_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_hotspot = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        # have BAGGED_DEAD_TREEs, click the house portal
        if (
                (datetime.datetime.now() - last_portal_click).total_seconds() > 8
                and qh.get_objects_v2('game', portal_id)
        ):
            res = osrs.move.right_click_v6(
                qh.get_objects_v2('game', portal_id)[0], "Build mode", qh.get_canvas(), in_inv=True
            )
            if res:
                last_portal_click = datetime.datetime.now()
        # i am in house
        elif qh.get_player_world_location('x') > 3500:
            if qh.get_chat_options('Build'):
                return osrs.keeb.write(str(qh.get_chat_options('Build')))
            elif qh.get_widgets(study_widget) and qh.get_widgets(study_widget)['xMin'] != -1:
                osrs.move.click(qh.get_widgets(study_widget))
                osrs.clock.random_sleep(1, 1.1)
            elif qh.get_widgets(rooms_holder) and qh.get_widgets(rooms_holder)['xMin'] != -1:
                osrs.move.fast_move(qh.get_widgets(rooms_holder))
                pyautogui.scroll(-1000)
            elif (qh.get_objects_v2('wall', hotspot, dist=5)
                  and (datetime.datetime.now() - last_hotspot).total_seconds() > 15):
                correct_location = list(
                    filter(
                        lambda obj: obj['y_coord'] < qh.get_player_world_location('y'), qh.get_objects_v2('wall', hotspot)
                    )
                )
                if correct_location:
                    res = osrs.move.right_click_v6(
                        correct_location[0],
                        'Build',
                        qh.get_canvas()
                    )
                    if res:
                        last_hotspot = datetime.datetime.now()
