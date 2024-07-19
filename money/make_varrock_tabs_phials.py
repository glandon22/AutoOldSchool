import datetime

import osrs

build_widget = '458,0'
built_chair = 6752
lectern = 13642
v_tab_widget = '403,20'


def leave_house():
    house_portal_id = 4525
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_orientation()
    qh.set_objects_v2('game', {house_portal_id})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') < 5000:
            return
        elif qh.get_objects_v2('game', house_portal_id):
            osrs.move.click_v2(
                qh.get_objects_v2('game', house_portal_id)[0],
                osrs.util.calculate_movement_offset(qh.get_orientation())
            )


def resupply():
    osrs.move.tab_to_varrock_v2()
    osrs.move.go_to_loc_v2(3165, 3483)
    osrs.bank.ge_handler_v2([
        {
            'id': osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value, 'sell': True,
            'quantity': '6500', 'id_override': 'varrock teleport'
        },
        {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.LAW_RUNE.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.SOFT_CLAY.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': 1}
    ])
    osrs.transport.house_tele_v2(outside=True)
    osrs.move.go_to_loc_v2(2954, 3216)


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main(min_SOFT_CLAYs):
    chat_input_widget = '162,42'
    create_widget = '403,14'
    portal_id = 15478
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_npcs_by_name(['phials'])
    qh.set_chat_options()
    qh.set_objects_v2('game', {built_chair, portal_id, lectern})
    qh.set_widgets({chat_input_widget, build_widget, v_tab_widget, create_widget})
    last_portal_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_phials_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_lectern_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_tab_make = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_create_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        # outside of house and no longer have more SOFT_CLAYs
        if (
                2944 <= qh.get_player_world_location('x') <= 2964
                and 3208 <= qh.get_player_world_location('y') <= 3232
                and not qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value + 1)
                and qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) < min_SOFT_CLAYs
        ):
            resupply()
        # exchange all noted SOFT_CLAYs with phials
        elif qh.get_chat_options('Exchange All', fuzzy=True):
            osrs.keeb.write_v2(qh.get_chat_options('Exchange All', fuzzy=True))
        # use SOFT_CLAYs on phials
        elif (
                qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) < min_SOFT_CLAYs
                and (datetime.datetime.now() - last_phials_click).total_seconds() > 8
                and len(qh.get_npcs_by_name()) > 0):
            osrs.move.click_v2(qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value + 1))
            n = qh.get_npcs_by_name()[0]
            c = qh.get_canvas()
            res = osrs.move.click_v2(n, right=[n, 'Use', c, True])
            if res:
                last_phials_click = datetime.datetime.now()
        # have SOFT_CLAYs, click the house portal
        elif (
                qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) >= min_SOFT_CLAYs
                and (datetime.datetime.now() - last_portal_click).total_seconds() > 8
                and qh.get_objects_v2('game', portal_id)
        ):
            o = qh.get_objects_v2('game', portal_id)[0]
            c = qh.get_canvas()
            res = osrs.move.click_v2(o, right=[o, 'Home', c, True])
            if res:
                last_portal_click = datetime.datetime.now()
        # i am in house
        elif qh.get_player_world_location('x') > 3500:
            # in house w SOFT_CLAYs, build!
            if qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) >= min_SOFT_CLAYs:
                # removing chair
                if (qh.get_objects_v2('game', lectern)
                        and (datetime.datetime.now() - last_lectern_click).total_seconds() > 10
                        and (datetime.datetime.now() - last_tab_make).total_seconds() > 60
                ):
                    o = qh.get_objects_v2('game', lectern)[0]
                    c = qh.get_canvas()
                    res = osrs.move.click_v2(o, right=[o, 'Study', c, True])
                    if res:
                        last_lectern_click = datetime.datetime.now()
                        # build chair + remove chair both first option
                elif qh.get_widgets(v_tab_widget) and (datetime.datetime.now() - last_tab_make).total_seconds() > 60:
                    osrs.move.click_v2(qh.get_widgets(v_tab_widget))
                    last_tab_make = datetime.datetime.now()
                elif qh.get_widgets(create_widget) and (
                            datetime.datetime.now() - last_create_click).total_seconds() > 5:
                    osrs.move.click_v2(qh.get_widgets(create_widget))
                    last_create_click = datetime.datetime.now()
            # out of SOFT_CLAYs - leave house
            else:
                osrs.player.toggle_run_v2('on')
                leave_house()
                last_tab_make = datetime.datetime.now() - datetime.timedelta(hours=1)
                last_create_click = datetime.datetime.now() - datetime.timedelta(hours=1)


main(1)

