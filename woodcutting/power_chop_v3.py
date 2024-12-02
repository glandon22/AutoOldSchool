import osrs

'''
***USAGE***
1. Set tree_to_cut to whichever tree type to cut
2. Position yourself near the tree you want to cut
3. Start script
'''

tree_to_cut = 'willow'

tree_map = {
    'regular': {1276, 1278, 1285},
    'oak': {10820},
    'willow': {10819, 10831, 10829, 10833},
    'maple': {10832},
    'yew': {10822, 10823},
    'magic': {10835},
    'redwood': {29668, 29670}
}


def am_cutting():
    # call this here bc the animation continues even after my bag is full
    # for a few game ticks
    manage_inventory()
    wc_animations = [
        879, 877, 875, 873, 871, 869, 867, 8303, 2846, 24, 2117, 7264, 8324, 8778
    ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_animation()
    qh.query_backend()
    if qh.get_player_animation() in wc_animations:
        return True


def manage_inventory():
    logs_to_drop = [
        osrs.item_ids.LOGS,
        osrs.item_ids.OAK_LOGS,
        osrs.item_ids.WILLOW_LOGS,
        osrs.item_ids.MAPLE_LOGS,
        osrs.item_ids.YEW_LOGS,
        osrs.item_ids.MAGIC_LOGS,
        osrs.item_ids.REDWOOD_LOGS,
    ]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_widgets({'270,14'})
    qh.query_backend()
    if qh.get_inventory() and len(qh.get_inventory()) == 28:
        if qh.get_inventory(osrs.item_ids.KNIFE) and qh.get_inventory(logs_to_drop):
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.KNIFE))
            osrs.move.fast_click_v2(qh.get_inventory(logs_to_drop))
            osrs.clock.sleep_one_tick()
            osrs.keeb.write('1')
            osrs.clock.random_sleep(45, 45.1)
        #osrs.inv.power_drop_v2(qh, logs_to_drop)
        # empty herb pouch for herbs i want
        if qh.get_inventory(30357):
            res = osrs.move.right_click_v6(
                qh.get_inventory(30357), 'Withdraw', qh.get_canvas(), in_inv=True
            )
            if res:
                osrs.clock.sleep_one_tick()
                osrs.clock.sleep_one_tick()
                osrs.keeb.write('8')
                osrs.clock.sleep_one_tick()
                osrs.clock.sleep_one_tick()
                osrs.keeb.write('30')
                osrs.keeb.press_key('enter')


while True:
    osrs.game.break_manager_v4({
        'intensity': 'low',
        'login': False,
        'logout': False
    })
    osrs.move.interact_with_object_v3(
        tree_map[tree_to_cut], custom_exit_function=am_cutting, pre_interact=manage_inventory,
        right_click_option='Chop down', timeout=7
    )
