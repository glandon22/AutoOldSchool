import random
import datetime

import osrs
fish_to_cut = [
    osrs.item_ids.BLUEGILL,
    osrs.item_ids.COMMON_TENCH,
    osrs.item_ids.MOTTLED_EEL,
    osrs.item_ids.GREATER_SIREN,
]

equipment = [
    {'id': osrs.item_ids.ANGLER_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.ANGLER_HAT, 'consume': 'Wear'},
    {'id': osrs.item_ids.ANGLER_WADERS, 'consume': 'Wear'},
    {'id': osrs.item_ids.ANGLER_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KNIFE,
    {'id': osrs.item_ids.FISH_CHUNKS, 'quantity': 'All'},
]


def select_molch():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.query_backend()
    if qh.get_chat_options('Molch Island', fuzzy=True):
        osrs.keeb.write(str(qh.get_chat_options('Molch', fuzzy=True)))


def start():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 1358 <= qh.get_player_world_location('x') <= 1376 and 3624 <= qh.get_player_world_location('y') <= 3641:
        osrs.dev.logger.info('Already in Molch, no need to run starter function.')
        return
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'aerial', 'items': equipment}]
    })
    osrs.game.tele_home()
    osrs.game.click_restore_pool()
    osrs.game.tele_home_fairy_ring('djr')
    osrs.move.go_to_loc(1435, 3650)
    osrs.move.go_to_loc(1415, 3612)
    osrs.move.interact_with_object_v3(
        33614, right_click_option='Board', timeout=3, coord_type='x', coord_value=1376, greater_than=False,
        pre_interact=select_molch
    )
    osrs.player.unequip(['weapon', 'gloves'])
    osrs.game.talk_to_npc('Alry the Angler', right_click=True, right_click_option='Get bird')
    osrs.game.dialogue_handler([], timeout=2)
    osrs.move.go_to_loc(1360, 3635)


def main(endless_loop=True):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.player_world_location()
    qh.set_projectiles_v2()
    qh.set_player_world_location()
    qh.npcs(['8523'])
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    last_cut = datetime.datetime.now() - datetime.timedelta(hours=1)
    start()
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
        bird_in_flight = list(filter(
            lambda bird: 'target' in bird and bird['target'] == 'UtahDogs', qh.get_projectiles_v2()
        ))
        fishing_spots = qh.get_npcs()
        if bird_in_flight \
                and qh.get_inventory(fish_to_cut) \
                and (datetime.datetime.now() - last_cut).total_seconds() > 0.6:
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.KNIFE))
            osrs.move.fast_click_v2(qh.get_inventory(fish_to_cut))
            last_cut = datetime.datetime.now()
        # fishing spots are available and my bird is not flying
        elif fishing_spots and not bird_in_flight:
            c = osrs.util.find_closest_target_in_game(fishing_spots, qh.get_player_world_location())
            if c:
                osrs.move.fast_click_v2(c)
                continue
