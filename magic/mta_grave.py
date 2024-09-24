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
    if qh.get_inventory() and len(qh.get_inventory()) == 28:
        osrs.keeb.press_key('f6')
        return True


def inv_empty():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    print('9999', qh.get_inventory(fruit))
    return not qh.get_inventory(fruit)


def cast_bones():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({
        osrs.widget_ids.inv_inv_widget_id,
        osrs.widget_ids.bones_banana_spell_widget_id
    })
    item_last_clicked = True
    while True:
        qh.query_backend()
        if not qh.get_inventory(bones):
            osrs.keeb.press_key('esc')
            osrs.keeb.press_key('esc')
            print('ret')
            return
        elif qh.get_widgets(osrs.widget_ids.bones_banana_spell_widget_id) and item_last_clicked:
            osrs.move.fast_click_v2(qh.get_widgets(osrs.widget_ids.bones_banana_spell_widget_id))


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
        res = osrs.combat_utils.fast_food_handler(qh, 10)
        if not res:
            return osrs.game.logout()
        osrs.move.interact_with_object_v3(bone_pile_id, custom_exit_function=inv_full)
        cast_bones()
        osrs.move.interact_with_object_v3(chute, custom_exit_function=inv_empty)

main()