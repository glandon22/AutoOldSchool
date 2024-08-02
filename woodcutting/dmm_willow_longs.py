import datetime

import osrs

wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]


def main():
    shop_interface = '300,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_animation()
    qh.set_objects(
        {'3234,3244,0', '3235,3238,0'},
        {'10819'},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_canvas()
    qh.set_widgets({shop_interface})
    while True:
        qh.query_backend()
        if len(qh.get_inventory()) == 28:
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.KNIFE.value))
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LOGS.value))
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('3')
            start = datetime.datetime.now()
            while True:
                osrs.keeb.press_key('space')
                qh.query_backend()
                if not qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LOGS.value):
                    break
                elif (datetime.datetime.now() - start).total_seconds() > 60:
                    osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.KNIFE.value))
                    osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LOGS.value))
                    osrs.clock.sleep_one_tick()
                    osrs.keeb.write('3')
                    start = datetime.datetime.now()
            osrs.move.go_to_loc(3215, 3245)
            osrs.move.interact_with_object(
                1540, 'x', 3214, False, obj_type='wall', obj_tile={'x': 3215, 'y': 3245},
                intermediate_tile='3214,3245,0', right_click_option='Open'
            )
            osrs.game.talk_to_npc('Shop keeper', right_click=True)
            osrs.game.dialogue_handler(['Yes please. What are you selling?'], timeout=1.3)
            while True:
                qh.query_backend()
                if not qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LONGBOW_U.value):
                    osrs.keeb.press_key('esc')
                    osrs.keeb.press_key('esc')
                    break
                elif qh.get_widgets(shop_interface) and qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LONGBOW_U.value):
                    osrs.move.right_click_v6(
                        qh.get_inventory(osrs.item_ids.ItemIDs.WILLOW_LONGBOW_U.value),
                        'Sell 50<col=ff9040>',
                        qh.get_canvas(),
                        in_inv=True
                    )
            osrs.move.interact_with_object(
                1540, 'x', 3215, True, obj_type='wall', obj_tile={'x': 3215, 'y': 3245},
                intermediate_tile='3215,3245,0', right_click_option='Open'
            )
            osrs.move.go_to_loc(3235, 3234, right_click=True)

        elif qh.get_player_animation() not in wc_animations and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '10819'):
            osrs.game.break_manager_v4({
                'login': False,
                'logout': False,
                'intensity': 'low'
            })
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, '10819')[0])


main()