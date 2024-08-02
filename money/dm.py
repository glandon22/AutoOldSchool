import datetime

import osrs

build_widget = '458,0'
built_chair = 6752
lectern = 13642
v_tab_widget = '403,20'

def resupply():
    osrs.move.tab_to_varrock()
    osrs.move.go_to_loc(3165, 3483)
    osrs.bank.ge_handler([
        {
            'id': osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value, 'sell': True,
            'quantity': 'All', 'id_override': 'varrock teleport'
        },
        {'id': osrs.item_ids.ItemIDs.FIRE_RUNE.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.LAW_RUNE.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.SOFT_CLAY.value, 'quantity': 13000},
        {'id': osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value, 'quantity': 1}
    ])
    osrs.transport.house_tele(outside=True)
    osrs.move.go_to_loc(2954, 3216)

script_config = {
    'intensity': 'low',
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
    last_home_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_var_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_lectern_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_tab_make = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_create_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if not qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) \
                and qh.get_player_world_location('x') < 3500:
            osrs.game.break_manager_v4(script_config)
            qh.query_backend()
        # in varrock need to resupply
        if not qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) \
                and qh.get_player_world_location('x') < 3500:
            if 3203 <= qh.get_player_world_location('x') <= 3223 and 3418 <= qh.get_player_world_location('y') <= 3437:
                osrs.bank.banking_handler({
                    'deposit': [
                        {
                            'id': osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value,
                            'quantity': 'All'
                        }
                    ],
                    'withdraw': [{'items': [osrs.item_ids.ItemIDs.SOFT_CLAY.value]}]
                })
                osrs.clock.sleep_one_tick()

        elif qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) \
                and qh.get_player_world_location('x') < 3500 and (datetime.datetime.now() - last_home_click).total_seconds() > 12:
            osrs.game.cast_spell('218,31')
            last_home_click = datetime.datetime.now()
        # i am in house
        elif qh.get_player_world_location('x') > 3500:
            # in house w SOFT_CLAYs, build!
            if qh.get_inventory(osrs.item_ids.ItemIDs.SOFT_CLAY.value, quantity=True) >= min_SOFT_CLAYs:
                # removing chair
                if (qh.get_objects_v2('game', lectern)
                        and (datetime.datetime.now() - last_lectern_click).total_seconds() > 10
                        and (datetime.datetime.now() - last_tab_make).total_seconds() > 70
                ):
                    res = osrs.move.right_click_v6(
                        qh.get_objects_v2('game', lectern)[0],
                        'Study',
                        qh.get_canvas(),
                    )
                    if res:
                        last_lectern_click = datetime.datetime.now()
                        # build chair + remove chair both first option
                elif qh.get_widgets(v_tab_widget) and (datetime.datetime.now() - last_tab_make).total_seconds() > 70:
                    osrs.move.click(qh.get_widgets(v_tab_widget))
                    last_tab_make = datetime.datetime.now()
                elif qh.get_widgets(create_widget) and (
                            datetime.datetime.now() - last_create_click).total_seconds() > 5:
                    osrs.move.click(qh.get_widgets(create_widget))
                    last_create_click = datetime.datetime.now()
            # out of SOFT_CLAYs - leave house
            elif (datetime.datetime.now() - last_var_click).total_seconds() > 10:
                osrs.game.cast_spell('218,23')
                # '218,31'
                last_var_click = datetime.datetime.now()
                last_tab_make = datetime.datetime.now() - datetime.timedelta(hours=1)
                last_create_click = datetime.datetime.now() - datetime.timedelta(hours=1)


main(1)

