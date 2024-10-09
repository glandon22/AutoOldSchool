import pyautogui

import osrs

bone_pile_id = {10725, 10726, 10727, 10728}
bones = [6904, 6905, 6906, 6907]
chute = 10735
fruit = [osrs.item_ids.PEACH, osrs.item_ids.BANANA]


def inv_full():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory() and osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), bones) >= 14:
        osrs.keeb.press_key('f6')
        return True


def inv_empty():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    return not qh.get_inventory(fruit)


def cast_bones():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({
        osrs.widget_ids.inv_inv_widget_id,
        osrs.widget_ids.bones_peaches_spell_widget_id
    })
    item_last_clicked = True
    while True:
        qh.query_backend()
        if not qh.get_inventory(bones) and qh.get_inventory(osrs.item_ids.PEACH):
            osrs.keeb.press_key('esc')
            osrs.keeb.press_key('esc')
            print('ret')
            return
        elif qh.get_widgets(osrs.widget_ids.bones_peaches_spell_widget_id) and item_last_clicked:
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.bones_peaches_spell_widget_id))


def resupply():
    osrs.move.interact_with_object_v3(23677, coord_type='y', coord_value=5000, greater_than=False)
    osrs.game.standard_spells_tele('Varrock')
    osrs.bank.banking_handler({
        'search': [{'query': 'shark', 'items': [{'id': osrs.item_ids.SHARK, 'quantity': '10'}]}]
    })
    osrs.game.dueling_tele("Emir's Arena")
    osrs.move.go_to_loc(3304, 3235)
    osrs.move.go_to_loc(3324, 3278)
    osrs.move.go_to_loc(3363, 3295)
    osrs.move.interact_with_object_v3(10721, coord_type='y', coord_value=3299, timeout=15, greater_than=True)
    osrs.move.interact_with_object_v3(
        23676, coord_type='y', coord_value=5000, intermediate_tile='3363,3307,0', greater_than=True,
        right_click_option='Enter', timeout=7
    )


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'hitpoints'})
    qh.set_inventory()
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'low',
            'login': False,
            'logout': False
        })
        qh.query_backend()
        osrs.move.interact_with_object_v3(bone_pile_id, custom_exit_function=inv_full)
        cast_bones()
        qh.query_backend()
        res = osrs.combat_utils.fast_food_handler(qh, 10)
        if not res:
            resupply()
        osrs.move.interact_with_object_v3(chute, custom_exit_function=inv_empty)

main()
