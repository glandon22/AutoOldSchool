import pyautogui

import osrs

items_to_alch = [
    6895, 6894, 6896, 6893, 6897
]


def find_best_tower():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_mta_data()
    qh.query_backend()
    if qh.get_mta_data() and 'getAlchItem' in qh.get_mta_data():
        return qh.get_mta_data()['getAlchItem']


def have_alchables():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_mta_data()
    qh.query_backend()
    if qh.get_inventory(items_to_alch):
        return True
    elif not qh.get_mta_data() or ('getAlchItem' in qh.get_mta_data() and qh.get_mta_data()['getAlchItem'] == {}):
        return True


def cast_alch():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({
        osrs.widget_ids.inv_inv_widget_id,
        osrs.widget_ids.high_alch_spell_widget_id
    })
    item_last_clicked = True
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        qh.query_backend()
        if not qh.get_inventory(items_to_alch):
            osrs.keeb.press_key('esc')
            osrs.keeb.press_key('esc')
            osrs.clock.random_sleep(0.1, 0.11)
            pyautogui.click()
            return
        elif qh.get_widgets(osrs.widget_ids.inv_inv_widget_id) and \
                qh.get_widgets(osrs.widget_ids.inv_inv_widget_id)['spriteID'] == 1030 \
                and osrs.inv.are_items_in_inventory_v2(reversed(qh.get_inventory()), items_to_alch) \
                and not item_last_clicked:
            osrs.move.fast_click_v2(
                osrs.inv.are_items_in_inventory_v2(reversed(qh.get_inventory()), items_to_alch)
            )
            item_last_clicked = True
        elif qh.get_widgets(osrs.widget_ids.high_alch_spell_widget_id) and item_last_clicked:
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.high_alch_spell_widget_id))
            item_last_clicked = False


def main():
    while True:
        targ = find_best_tower()
        if not targ:
            osrs.move.interact_with_object_v3(
                {23679, 23689, 23687, 23685, 23683, 23681}, custom_exit_function=find_best_tower,
                right_click_option='Search', timeout=7
            )
        else:
            osrs.move.interact_with_object_v3(
                targ['id'], custom_exit_function=have_alchables, right_click_option='Take-5', timeout=7
            )
        osrs.keeb.press_key('f6')
        cast_alch()


main()