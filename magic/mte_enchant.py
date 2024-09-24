import osrs


def full_inv():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory() and len(qh.get_inventory()) == 28:
        return True


def begin_casting():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'161,65', osrs.widget_ids.enchant_sub_menu_widget_id, osrs.widget_ids.l6_enchant_menu_widget_id})
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_widgets(osrs.widget_ids.l6_enchant_menu_widget_id):
            return
        elif qh.get_widgets(osrs.widget_ids.enchant_sub_menu_widget_id):
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.enchant_sub_menu_widget_id))
        elif qh.get_widgets('161,65') and qh.get_widgets('161,65')['spriteID'] != 1027:
            osrs.keeb.press_key('f6')


def cast_enchant():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({
        osrs.widget_ids.inv_inv_widget_id,
        osrs.widget_ids.l6_enchant_menu_widget_id
    })
    item_last_clicked = True
    while True:
        qh.query_backend()
        if not qh.get_inventory([osrs.item_ids.CYLINDER, osrs.item_ids.DRAGONSTONE_6903]):
            osrs.keeb.press_key('esc')
            osrs.keeb.press_key('esc')
            return
        elif qh.get_widgets(osrs.widget_ids.inv_inv_widget_id) and \
                qh.get_widgets(osrs.widget_ids.inv_inv_widget_id)['spriteID'] == 1030 \
                and osrs.inv.are_items_in_inventory_v2(reversed(qh.get_inventory()), [osrs.item_ids.CYLINDER, osrs.item_ids.DRAGONSTONE_6903]) \
                and not item_last_clicked:
            osrs.move.fast_click_v2(
                osrs.inv.are_items_in_inventory_v2(reversed(qh.get_inventory()), [osrs.item_ids.CYLINDER, osrs.item_ids.DRAGONSTONE_6903])
            )
            item_last_clicked = True
        elif qh.get_widgets(osrs.widget_ids.l6_enchant_menu_widget_id) and item_last_clicked:
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.l6_enchant_menu_widget_id))
            item_last_clicked = False


def drop_all():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    osrs.inv.power_drop_v2(qh, [osrs.item_ids.ORB_6902])


def main():
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        osrs.move.interact_with_object_v3(23695, custom_exit_function=full_inv)
        begin_casting()
        cast_enchant()
        drop_all()

main()
