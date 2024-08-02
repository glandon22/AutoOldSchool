import datetime

import osrs

build_widget = '458,0'
built_chair = 6752
chair_space = 4517


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
    'login': lambda: osrs.clock.random_sleep(3, 3.1),
    'logout': False
}


def main(min_planks):
    chat_input_widget = '162,42'
    portal_id = 15478
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_npcs_by_name(['phials'])
    qh.set_chat_options()
    qh.set_objects_v2('game', {built_chair, portal_id, chair_space})
    qh.set_widgets({chat_input_widget, build_widget})
    last_portal_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_phials_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_chair_build = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_chair_removal = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        # outside of house and no longer have more planks
        if (
                2944 <= qh.get_player_world_location('x') <= 2964
                and 3208 <= qh.get_player_world_location('y') <= 3232
                and not qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value + 1)
                and qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value, quantity=True) < min_planks
        ):
            return
        # exchange all noted planks with phials
        elif qh.get_chat_options('Exchange All', fuzzy=True):
            osrs.keeb.write(str(qh.get_chat_options('Exchange All', fuzzy=True)))
        # use planks on phials
        elif (
                qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value, quantity=True) < min_planks
                and (datetime.datetime.now() - last_phials_click).total_seconds() > 8
                and len(qh.get_npcs_by_name()) > 0):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value + 1))
            res = osrs.move.right_click_v6(qh.get_npcs_by_name()[0], 'Use', qh.get_canvas(), in_inv=True)
            if res:
                last_phials_click = datetime.datetime.now()
        # have planks, click the house portal
        elif (
                qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value, quantity=True) >= min_planks
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
            # in house w planks, build!
            if qh.get_inventory(osrs.item_ids.ItemIDs.PLANK.value, quantity=True) >= min_planks:
                # removing chair
                if (qh.get_objects_v2('game', built_chair)
                        and (datetime.datetime.now() - last_chair_removal).total_seconds() > 4):
                    res = osrs.move.right_click_v6(
                        qh.get_objects_v2('game', built_chair)[0],
                        'Remove',
                        qh.get_canvas(),
                    )
                    if res:
                        last_chair_removal = datetime.datetime.now()
                # build chair + remove chair both first option
                elif qh.get_widgets(build_widget) or qh.get_chat_options():
                    osrs.keeb.write('1')
                # empty chair space - build a char
                elif (qh.get_objects_v2('game', chair_space)
                      and (datetime.datetime.now() - last_chair_build).total_seconds() > 4):
                    res = osrs.move.right_click_v6(
                        qh.get_objects_v2('game', chair_space)[0],
                        'Build',
                        qh.get_canvas(),
                    )
                    if res:
                        last_chair_build = datetime.datetime.now()
            # out of planks - leave house
            else:
                leave_house()
