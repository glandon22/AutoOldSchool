import datetime
import random

import osrs

bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]

molten_glass_id = '1775'
pipe_id = '1785'


deposit_query = [
    {
        'id': osrs.item_ids.BEER_GLASS,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.EMPTY_CANDLE_LANTERN,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.EMPTY_OIL_LAMP,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.EMPTY_OIL_LANTERN,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.EMPTY_VIAL,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.EMPTY_FISHBOWL,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.UNPOWERED_ORB,
        'quantity': 'All'
    },
]


def determine_item_to_make(lvl):
    if lvl < 4:
        return '1'
    elif lvl < 12:
        return '2'
    elif lvl < 33:
        return '3'
    elif lvl < 42:
        return '4'
    elif lvl < 46:
        return '5'
    elif lvl < 100:
        return '6'


def open_bank_interface(qh: osrs.queryHelper.QueryHelper):
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        bank_data = qh.get_bank()
        if bank_data:
            return
        elif (datetime.datetime.now() - last_click).total_seconds() > 7:
            closest = osrs.util.find_closest_target(qh.get_npcs())
            if not closest:
                continue
            osrs.move.click(closest)
            last_click = datetime.datetime.now()


def withdraw_materials_v3(qh: osrs.queryHelper.QueryHelper):
    qh.query_backend()
    if not qh.get_bank():
        return
    glass = qh.get_bank(molten_glass_id)
    if not glass:
        exit('out of glass')
    osrs.move.click(glass)
    osrs.keeb.keyboard.press(osrs.keeb.key.esc)
    osrs.keeb.keyboard.release(osrs.keeb.key.esc)
    start_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_inventory(molten_glass_id):
            break
        elif (datetime.datetime.now() - start_time).total_seconds() > 5:
            break


script_config = {
    'intensity': 'low',
    'login': lambda: osrs.clock.random_sleep(3, 4),
    'logout': False
}


def main(goal_level=99):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_skills({'crafting'})
    qh.set_widgets({'233,0', '270,14'})
    qh.set_npcs(bankers_ids)
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_banked = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        if qh.get_skills('crafting') and qh.get_skills('crafting')['level'] >= goal_level:
            return

        glass = qh.get_inventory(molten_glass_id)
        pipe = qh.get_inventory(pipe_id)
        if not pipe:
            qh.set_script_stats({'status': 'ERROR: Could not find pipe.'})
            exit('no pipe')
        if not glass and (datetime.datetime.now() - last_banked).total_seconds() > 3:
            osrs.bank.banking_handler({
                'deposit': deposit_query,
                'withdraw': [{'items': [{'id': osrs.item_ids.MOLTEN_GLASS, 'quantity': 'All'}]}]
            })
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            last_banked = datetime.datetime.now()
        elif glass and (datetime.datetime.now() - last_click).total_seconds() > 60:
            qh.set_script_stats({'status': 'Crafting items.'})
            osrs.move.click(pipe)
            osrs.move.click(glass)
            wait_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_widgets('270,14'):
                    lvl = qh.get_skills('crafting')
                    osrs.keeb.keyboard.type(determine_item_to_make(lvl['level']))
                    last_click = datetime.datetime.now()
                    if random.randint(0, 10) == 1:
                        osrs.move.jiggle_mouse()
                    break
                elif (datetime.datetime.now() - wait_time).total_seconds() > 4:
                    break
        elif qh.get_widgets('233,0'):
            qh.set_script_stats({'status': 'Leveled up!'})
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
