import datetime

import osrs

def dump_inv_right_click(qh: osrs.queryHelper.QueryHelper, items_to_drop: list):
    for item in qh.get_inventory():
        if item['id'] in items_to_drop:
            osrs.move.right_click_v6(item, 'Drop', qh.get_canvas(), in_inv=True)


def main(goal_lvl=99):
    last_steal = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_drop = datetime.datetime.now() - datetime.timedelta(hours=1)
    tea_stall = 11730
    currently_fletching = True
    arrow_widget = '270,14'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_widgets({arrow_widget})
    qh.set_objects_v2('game', {tea_stall})
    qh.set_skills({'thieving'})
    last_arrow_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': None,
            'logout': None,
        })
        qh.query_backend()
        if qh.get_skills('thieving') and qh.get_skills('thieving')['level'] >= goal_lvl:
            return

        if len(qh.get_inventory()) > 0 and (datetime.datetime.now() - last_drop).total_seconds() > 0.6:
            dump_inv_right_click(qh, [osrs.item_ids.ItemIDs.CAKE.value, osrs.item_ids.ItemIDs.BREAD.value, osrs.item_ids.ItemIDs.CHOCOLATE_SLICE.value])
            last_drop = datetime.datetime.now()
        elif qh.get_objects_v2('game', tea_stall) and (datetime.datetime.now() - last_steal).total_seconds() > 1.2:
            osrs.move.fast_click(qh.get_objects_v2('game', tea_stall)[0])
            currently_fletching = False
            last_steal = datetime.datetime.now()
        elif not currently_fletching:
            if qh.get_widgets(arrow_widget):
                osrs.keeb.press_key('space')
                currently_fletching = True
            elif qh.get_inventory(osrs.item_ids.ItemIDs.ARROW_SHAFT.value) \
                and qh.get_inventory(osrs.item_ids.ItemIDs.FEATHER.value) and \
                    (datetime.datetime.now() - last_arrow_click).total_seconds() > 0.7:
                osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.ARROW_SHAFT.value))
                osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.FEATHER.value))
                last_arrow_click = datetime.datetime.now()


main()