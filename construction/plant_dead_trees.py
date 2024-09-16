import datetime

import pyautogui

import osrs

build_widget = '458,0'
planted_tree = 4531
tree_space = 15362
watering_can_list = [
    osrs.item_ids.WATERING_CAN1,
    osrs.item_ids.WATERING_CAN2,
    osrs.item_ids.WATERING_CAN3,
    osrs.item_ids.WATERING_CAN4,
    osrs.item_ids.WATERING_CAN5,
    osrs.item_ids.WATERING_CAN6,
    osrs.item_ids.WATERING_CAN7,
    osrs.item_ids.WATERING_CAN,
]

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
    chat_input_widget = '162,42'
    portal_id = 15478
    sink_id = 9684
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_npcs_by_name(['phials'])
    qh.set_chat_options()
    qh.set_objects_v2('game', {planted_tree, portal_id, tree_space, sink_id})
    qh.set_widgets({chat_input_widget, build_widget})
    last_portal_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_phials_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_chair_build = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_chair_removal = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_can_fill = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        # outside of house and no longer have more BAGGED_DEAD_TREEs
        if (
                2944 <= qh.get_player_world_location('x') <= 2964
                and 3208 <= qh.get_player_world_location('y') <= 3232
                and not qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE + 1)
                and not qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE)
        ):
            return
        # exchange all noted BAGGED_DEAD_TREEs with phials
        elif qh.get_chat_options('Exchange All', fuzzy=True):
            osrs.keeb.write(str(qh.get_chat_options('Exchange All', fuzzy=True)))
        # use BAGGED_DEAD_TREEs on phials
        elif (
                not qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE)
                and qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE + 1)
                and (datetime.datetime.now() - last_phials_click).total_seconds() > 8
                and len(qh.get_npcs_by_name()) > 0):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE + 1))
            res = osrs.move.right_click_v6(qh.get_npcs_by_name()[0], 'Use', qh.get_canvas(), in_inv=True)
            if res:
                last_phials_click = datetime.datetime.now()
        # fill watering cans
        elif qh.get_inventory(watering_can_list) and qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE) and qh.get_player_world_location('x') < 3500:
            if (qh.get_objects_v2('game', sink_id)
                    and (datetime.datetime.now() - last_can_fill).total_seconds() > 30):
                osrs.move.click(qh.get_inventory(watering_can_list))
                res = osrs.move.right_click_v6(
                    qh.get_objects_v2('game', sink_id)[0],
                    'Use',
                    qh.get_canvas()
                )
                if res:
                    last_can_fill = datetime.datetime.now()
            elif not qh.get_objects_v2('game', sink_id):
                osrs.move.go_to_loc(2960, 3213)
        # have BAGGED_DEAD_TREEs, click the house portal
        elif (
                qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE)
                and (datetime.datetime.now() - last_portal_click).total_seconds() > 8
                and qh.get_objects_v2('game', portal_id)
        ):
            res = osrs.move.right_click_v6(
                qh.get_objects_v2('game', portal_id)[0], "Build mode", qh.get_canvas(), in_inv=True
            )
            if res:
                last_portal_click = datetime.datetime.now()
        # i am in house
        elif qh.get_player_world_location('x') > 3500:
            # in house w BAGGED_DEAD_TREEs, build!
            if qh.get_inventory(osrs.item_ids.BAGGED_DEAD_TREE):
                # removing chair
                if (qh.get_objects_v2('game', planted_tree)
                        and (datetime.datetime.now() - last_chair_removal).total_seconds() > 4):
                    res = osrs.move.right_click_v6(
                        qh.get_objects_v2('game', planted_tree)[0],
                        'Remove',
                        qh.get_canvas(),
                    )
                    if res:
                        last_chair_removal = datetime.datetime.now()
                # build chair + remove chair both first option
                elif qh.get_widgets(build_widget) or qh.get_chat_options():
                    osrs.keeb.write('1')
                # empty chair space - build a char
                elif (qh.get_objects_v2('game', tree_space)
                      and (datetime.datetime.now() - last_chair_build).total_seconds() > 4):
                    res = osrs.move.right_click_v6(
                        qh.get_objects_v2('game', tree_space)[0],
                        'Build',
                        qh.get_canvas(),
                    )
                    if res:
                        last_chair_build = datetime.datetime.now()
            # out of BAGGED_DEAD_TREEs - leave house
            else:
                leave_house()
