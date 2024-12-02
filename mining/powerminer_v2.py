import datetime
import random

import osrs

'''
***USAGE***
1. Set rock_to_mine to whichever rock you want to mine
2. Position yourself near the rock you want to mine
3. Start script
'''

rock_map = {
    'copper': {10943, 11161},
    'tin': {11361, 11360, 11368, 11369},
    'iron': {11364, 11365},
    'coal': {11366, 11367},
    'mith': {11372, 11373},
    'addy': {11374, 11375},
    'rune': {11377, 11376},
    'silver': {11368, 11369},
    'gold': {11370, 11371},
}

ore_to_drop = [
    osrs.item_ids.TIN_ORE,
    osrs.item_ids.COPPER_ORE,
    osrs.item_ids.IRON_ORE,
    osrs.item_ids.SILVER_ORE,
    osrs.item_ids.GOLD_ORE,
    osrs.item_ids.COAL,
    osrs.item_ids.MITHRIL_ORE,
    osrs.item_ids.ADAMANTITE_ORE,
    osrs.item_ids.RUNITE_ORE,
]


equipment = [
    {'id': osrs.item_ids.DRAGON_PICKAXE}, # chagne this whatever the leageues pickax is if i take that
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    {'id': osrs.item_ids.RUNE_POUCH},
]


def start_function():
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'mlm', 'items': equipment}]
    })
    osrs.game.tele_home_v2()
    osrs.game.tele_home_fairy_ring('cir')
    osrs.move.go_to_loc(1321, 3763, skip_dax=True)
    osrs.move.go_to_loc(1323, 3775)
    osrs.move.interact_with_object_v3(34397, 'y', 3780)
    osrs.move.interact_with_object_v3(34396, 'y', 3790)
    osrs.move.go_to_loc(1277, 3814)


def main(endless_loop=False, rock_to_mine='iron'):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_is_mining()
    qh.set_widgets({'387,20'})
    qh.set_objects_v2('game', rock_map[rock_to_mine])
    if not endless_loop:
        start_function()
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    last_herb = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        break_info = osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        if iter_count == 0:
            return
        elif 'took_break' in break_info and break_info['took_break']:
            iter_count -= 1
        qh.query_backend()
        rocks = qh.get_objects_v2('game')
        if qh.get_inventory() and len(qh.get_inventory()) == 28:
            osrs.dev.logger.info('Ore in inventory, dropping.')
            osrs.inv.power_drop_v2(qh, ore_to_drop)
        elif (datetime.datetime.now() - last_herb).total_seconds() > 60:
            osrs.keeb.press_key('f4')
            if qh.get_widgets('387,20'):
                res = osrs.move.right_click_v6(
                    qh.get_widgets('387,20'), 'Withdraw-last', qh.get_canvas(), in_inv=True
                )
                osrs.keeb.press_key('esc')
                if res:
                    last_herb = datetime.datetime.now()
        elif qh.get_is_mining():
            osrs.dev.logger.info('Currently mining.')
            continue
        # dont click more than 1 tick
        elif rocks and (datetime.datetime.now() - last_click).total_seconds() > 0.61:
            osrs.dev.logger.info('Clicking a new rock to mine.')
            closest = osrs.util.find_closest_target_on_screen(rocks)
            if closest:
                osrs.move.fast_click_v2(closest)
                last_click = datetime.datetime.now()


main(endless_loop=True, rock_to_mine='rune')