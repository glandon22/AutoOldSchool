import datetime

import osrs


def repair_pouches():
    # have runes for spell s[rite-d =568
    main_chat_widget = '162,34'
    mage_widget = '75,12'
    spellbook_widget = '161,65'
    contact_widget = '218,108'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({mage_widget, spellbook_widget, contact_widget, main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(mage_widget):
            osrs.move.click(qh.get_widgets(mage_widget))
            osrs.clock.random_sleep(3, 3.1)
            osrs.keeb.press_key('esc')
            break
        elif qh.get_widgets(spellbook_widget) and qh.get_widgets(spellbook_widget)['spriteID'] != 1027:
            osrs.keeb.press_key('f6')
        elif qh.get_widgets(contact_widget) \
                and not qh.get_widgets(contact_widget)['isHidden'] \
                and qh.get_widgets(contact_widget)['spriteID'] == 568:
            osrs.move.click(qh.get_widgets(contact_widget))
    osrs.player.dialogue_handler(["Can you repair my pouches?"])


def cast_magic_imbue():
    spellbook_widget = '161,65'
    imbue_widget = '218,128'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({spellbook_widget, imbue_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(spellbook_widget) and qh.get_widgets(spellbook_widget)['spriteID'] != 1027:
            osrs.keeb.press_key('f6')
        elif qh.get_widgets(imbue_widget) \
                and not qh.get_widgets(imbue_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(imbue_widget))
            osrs.keeb.press_key('esc')
            return


def click_pouches(qh, empty=False):
    if empty:
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.GIANT_POUCH.value),
            'Empty',
            qh.get_canvas(),
            in_inv=True
        )
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.LARGE_POUCH.value),
            'Empty',
            qh.get_canvas(),
            in_inv=True
        )
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.MEDIUM_POUCH.value),
            'Empty',
            qh.get_canvas(),
            in_inv=True
        )
    else:
        osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.GIANT_POUCH.value))
        osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.LARGE_POUCH.value))
        osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.MEDIUM_POUCH.value))


def fill_pouches(qh):
    qh.query_backend()
    osrs.bank.banking_handler({
        'withdraw': [{'items': [{
            'id': osrs.item_ids.ItemIDs.PURE_ESSENCE.value,
            'quantity': 'All'
        }]}]
    })
    click_pouches(qh)


def tele_to_earth_altar():
    ring_widget = '387,24'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_widgets({ring_widget})
    qh.set_canvas()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.keeb.press_key('f4')
        qh.query_backend()
        if 3277 <= qh.get_player_world_location('x') <= 3303 and 3459 <= qh.get_player_world_location('y') <= 3482:
            osrs.keeb.press_key('esc')
            return
        elif qh.get_widgets(ring_widget) \
                and not qh.get_widgets(ring_widget)['isHidden'] \
                and (datetime.datetime.now() - last_click).total_seconds() > 10:
            res = osrs.move.right_click_v6(qh.get_widgets(ring_widget), 'Earth Altar', qh.get_canvas(), in_inv=True)
            if res:
                last_click = datetime.datetime.now()


def click_water_rune():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_varbit('5438')
    qh.query_backend()
    if not qh.get_varbit():
        cast_magic_imbue()
    if qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value):
        osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value))


def crafted_runes():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.PURE_ESSENCE.value):
        return True


def make_muds(qh, final_run=False):
    osrs.move.interact_with_object(
        34763, 'y', 4800, True, pre_interact=click_water_rune,
        custom_exit_function=crafted_runes
    )
    # wait until my ess is back in inv before leaving
    if not final_run:
        click_pouches(qh, True)
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.ItemIDs.PURE_ESSENCE.value):
                return


def main(goal_lvl=99):
    iters = 1
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'runecraft'})
    qh.set_equipment()
    qh.set_inventory()
    qh.set_canvas()
    qh.query_backend()
    if qh.get_skills('runecraft') and qh.get_skills('runecraft')['level'] >= goal_lvl:
        return
    if iters % 5 == 0:
        osrs.bank.banking_handler({
            'withdraw': [{'items': [{
                'id': osrs.item_ids.ItemIDs.COSMIC_RUNE.value,
                'quantity': '1'
            }]}]
        })
        repair_pouches()

    if not qh.get_equipment(osrs.item_ids.ItemIDs.BINDING_NECKLACE.value):
        osrs.bank.banking_handler({
            'withdraw': [{'items': [{
                'id': osrs.item_ids.ItemIDs.BINDING_NECKLACE.value,
                'quantity': '1'
            }]}]
        })
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.ItemIDs.BINDING_NECKLACE.value):
                osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.BINDING_NECKLACE.value))
                break

    fill_pouches(qh)
    fill_pouches(qh)
    fill_pouches(qh)
    tele_to_earth_altar()
    # flash the spellbook screen so it loads in where the spell widget is
    osrs.keeb.press_key('f6')
    osrs.keeb.press_key('esc')
    osrs.move.interact_with_object(34816, 'y', 4800, True, intermediate_tile='3295,3469,0')
    # cast magic imbue then use the water runes on altar
    make_muds(qh)
    make_muds(qh)
    make_muds(qh, True)
    # need to update the bank function to be able to deposit singular items, shouldnt be that hard




main(99)


'''
23
45
50
'''