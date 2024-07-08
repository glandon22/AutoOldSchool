import datetime

import pyautogui

import osrs
import transport_functions
import util_functions

dialogue = [
    "You seem worried, what's up?", "I'd be happy to help!",
    "I'd be happy to help!", "Yes.",
    "I think so!",
    "None of the above.", "A man came to me with the King's seal.", "I gave the man Daconia rocks.",
    "And Daconia rocks will kill the tree!", "Climb Up.", "Climb Down.", "Take me to Karamja please!",
    "Glough sent me.", "Ka.", "Lu.", "Min.", "Sadly his wife is no longer with us!", "He loves worm holes.", "Anita.",
    "I suppose so."
]


def walk_out_of_c_wars():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2446,3090,0'})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2445:
            return
        elif qh.get_tiles('2446,3090,0'):
            osrs.move.fast_click(qh.get_tiles('2446,3090,0'))


def open_cupboard():
    cpb = 2435
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {cpb})
    qh.query_backend()
    if qh.get_objects_v2('game', cpb):
        return True


def get_journal():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLOUGHS_JOURNAL.value):
        return True


def enter_gate():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({util_functions.main_chat_widget})
    qh.query_backend()
    if qh.get_widgets(util_functions.main_chat_widget):
        return True


def click_key():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLOUGHS_KEY.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.GLOUGHS_KEY.value))


def get_plans():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.INVASION_PLANS.value):
        return True


def click_t():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS.value))


def place_t():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS.value):
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        return True


def click_u():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_790.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_790.value))


def place_u():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_790.value):
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        return True


def click_z():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_791.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_791.value))


def place_z():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_791.value):
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        return True


def click_o():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_792.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_792.value))


def place_o():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.TWIGS_792.value):
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        return True


def run_to_safe_spot(timeout, x, y, z=0):
    targ_tile = f'{x},{y},{z}'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({targ_tile})
    time_on_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == x and qh.get_player_world_location(
                'y') == y and qh.get_player_world_location('z') == z:
            if (datetime.datetime.now() - time_on_tile).total_seconds() > timeout:
                return
        else:
            time_on_tile = datetime.datetime.now()

        if (not (qh.get_player_world_location('x') == x
                 and qh.get_player_world_location('y') == y
                 and qh.get_player_world_location('z') == z)
                and qh.get_tiles(targ_tile)):
            osrs.move.fast_click(qh.get_tiles(targ_tile))


def run_to_safe_spot_with_anchor(timeout):
    ladder = 17028
    targ_tile = ''
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2('game', {ladder})
    time_on_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if targ_tile == '':
            if qh.get_objects_v2('game', ladder):
                ladder = qh.get_objects_v2('game', ladder)[0]
                targ_tile = {'x': ladder["x_coord"], 'y': ladder["y_coord"] + 1}
                qh.set_tiles({f'{targ_tile["x"]},{targ_tile["y"]},0'})
                print('set safe tile: ', f'{targ_tile["x"]},{targ_tile["y"]},0')
                print('vs player loc ', qh.get_player_world_location())
        elif qh.get_player_world_location('x') == targ_tile['x'] and qh.get_player_world_location(
                'y') == targ_tile['y']:
            if (datetime.datetime.now() - time_on_tile).total_seconds() > timeout:
                print('in loc greater than ', timeout)
                print(qh.get_player_world_location(), targ_tile)
                return
            continue
        elif qh.get_tiles(f'{targ_tile["x"]},{targ_tile["y"]},0'):
            osrs.move.right_click_v6(qh.get_tiles(f'{targ_tile["x"]},{targ_tile["y"]},0'), 'Walk here', qh.get_canvas(), in_inv=True)
        time_on_tile = datetime.datetime.now()


def kill_demon():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['black demon'])
    qh.set_interating_with()
    fought = False
    while True:
        run_to_safe_spot_with_anchor(0.6)
        qh.query_backend()
        if qh.get_npcs_by_name() and not qh.get_interating_with():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_interating_with():
            fought = True
            print('in combat')
        elif not qh.get_npcs_by_name() and fought:
            return
        osrs.keeb.press_key('space')


root_list = [
    {
        'tile': '2467,9896,0',
        'id': '1985'
    },
    {
        'tile': '2473,9897,0',
        'id': '1985'
    },
    {
        'tile': '2481,9904,0',
        'id': '1986'
    },
    # after the one above i need to walk to 2487,9891,0
    {
        'tile': '2490,9891,0',
        'id': '1985',
        'walk_to': '2487,9891,0'
    },
    {
        'tile': '2485,9887,0',
        'id': '1985'
    },
    # from here walk to 2471,9895,0
    {
        'tile': '2469,9874,0',
        'id': '1986',
        'walk_to': '2466,9881,0'
    },
    {
        'tile': '2457,9876,0',
        'id': '1986'
    },
    {
        'tile': '2445,9880,0',
        'id': '1985'
    },
    {
        'tile': '2441,9883,0',
        'id': '1986'
    },
    {
        'tile': '2446,9893,0',
        'id': '1986'
    },
    {
        'tile': '2452,9893,0',
        'id': '1985'
    },
    {
        'tile': '2456,9888,0',
        'id': '1985'
    },
    {
        'tile': '2457,9883,0',
        'id': '1986'
    },
    {
        'tile': '2465,9893,0',
        'id': '1986'
    },
    {
        'tile': '2468,9892,0',
        'id': '1986'
    }
]


def click_roots():
    for root in root_list:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_player_animation()
        qh.set_objects(
            {root['tile']},
            {root['id']},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        qh.set_widgets({util_functions.main_chat_widget})
        if 'walk_to' in root:
            qh.set_tiles({root['walk_to']})
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.ItemIDs.DACONIA_ROCK.value):
                return True
            elif qh.get_widgets(util_functions.main_chat_widget):
                osrs.keeb.press_key('space')
            elif qh.get_player_animation() == 827:
                osrs.clock.random_sleep(3, 3.1)
                break
            elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, root['id']):
                osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, root['id'])[0])
            elif 'walk_to' in root and qh.get_tiles(root['walk_to']):
                osrs.move.fast_click(qh.get_tiles(root['walk_to']))


def main():
    osrs.move.interact_with_object(1967, 'y', 3492, True)
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(10, 10.1)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=4)
    osrs.move.go_to_loc(2449, 3483, 1)
    quest_items = [
        osrs.item_ids.ItemIDs.TRANSLATION_BOOK.value,
        osrs.item_ids.ItemIDs.BARK_SAMPLE.value,
        {
            'id': [
                osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
                osrs.item_ids.ItemIDs.PRAYER_POTION3.value,
                osrs.item_ids.ItemIDs.PRAYER_POTION2.value,
                osrs.item_ids.ItemIDs.PRAYER_POTION1.value,
            ],
            'quantity': '1'
        },
        {
            'id': [
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE5.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE4.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE3.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE2.value,
            ],
            'quantity': '1'
        },
        {
            'id': [
                osrs.item_ids.ItemIDs.RING_OF_DUELING8.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING7.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING6.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING5.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING4.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING3.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING2.value,
                osrs.item_ids.ItemIDs.RING_OF_DUELING1.value,
            ],
            'quantity': '1'
        },
    ]
    osrs.bank.banking_handler({
        'dump_inv': True,
        'dump_equipment': True,
        'search': [{'query': '', 'items': quest_items}]
    })
    transport_functions.dueling_to_c_wars()
    walk_out_of_c_wars()
    osrs.move.go_to_loc(2669, 3111)
    osrs.player.toggle_run('on')
    osrs.move.go_to_loc(2677, 3094)
    osrs.move.interact_with_object(1543, 'y', 3088, False, obj_type='wall', intermediate_tile='2677,3088,0')
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=4)
    osrs.player.toggle_run('off')
    util_functions.talk_to_npc('hazelmere', right_click=True)
    util_functions.dialogue_handler(dialogue)
    transport_functions.necklace_of_passage_tele_outpost()
    transport_functions.walk_to_loc(2458, 2462, 3379, 3382, 2460, 3381)
    osrs.move.interact_with_object(190, 'y', 3384, True)
    osrs.move.go_to_loc(2465, 3489)
    osrs.move.interact_with_object(1967, 'y', 3492, True)
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(1967, 'y', 3491, False)
    osrs.move.go_to_loc(2474, 3459)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    util_functions.talk_to_npc('glough')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16679, 'z', 0, False, timeout=6)
    osrs.move.go_to_loc(2465, 3489)
    osrs.move.interact_with_object(1967, 'y', 3492, True)
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    osrs.move.interact_with_object(16684, 'z', 2, True, timeout=6, obj_dist=7, right_click_option='Climb-up')
    osrs.move.interact_with_object(2884, 'z', 3, True, timeout=6, obj_dist=7, right_click_option='Climb-up')
    util_functions.talk_to_npc('charlie')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16679, 'z', 2, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(2884, 'z', 1, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(16684, 'z', 0, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(1967, 'y', 3491, False)
    osrs.move.go_to_loc(2474, 3459)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    osrs.move.interact_with_object(2434, 'a', 1, True, custom_exit_function=open_cupboard)
    osrs.move.interact_with_object(2435, 'a', 1, True, custom_exit_function=get_journal)
    util_functions.talk_to_npc('glough')
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(10, 10.1)
    util_functions.talk_to_npc('charlie')
    util_functions.dialogue_handler(dialogue)
    osrs.player.toggle_run('on')
    util_functions.talk_to_npc('captain errdo', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2944, 3042)
    osrs.move.interact_with_object(2439, 'a', 1, True, obj_type='wall', custom_exit_function=enter_gate)
    util_functions.dialogue_handler(dialogue)
    osrs.player.toggle_run('off')
    osrs.move.go_to_loc(3001, 3045)
    util_functions.talk_to_npc('foreman', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(10, 10.1)
    util_functions.talk_to_npc('foreman', right_click=True)
    util_functions.dialogue_handler(dialogue)
    transport_functions.necklace_of_passage_tele_outpost()
    transport_functions.walk_to_loc(2458, 2462, 3379, 3382, 2460, 3381)
    util_functions.talk_to_npc('femi', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2465, 3489)
    osrs.move.interact_with_object(1967, 'y', 3492, True)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    osrs.move.interact_with_object(16684, 'z', 2, True, timeout=6, obj_dist=7, right_click_option='Climb-up')
    osrs.move.interact_with_object(2884, 'z', 3, True, timeout=6, obj_dist=7, right_click_option='Climb-up')
    util_functions.talk_to_npc('charlie')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16679, 'z', 2, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(2884, 'z', 1, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(16684, 'z', 0, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(1967, 'y', 3491, False)
    osrs.move.go_to_loc(2393, 3511)
    osrs.move.interact_with_object(16675, 'z', 1, True, timeout=6, obj_dist=7)
    util_functions.talk_to_npc('anita')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16677, 'z', 0, False, timeout=6, obj_dist=7)
    osrs.move.go_to_loc(2474, 3459)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    osrs.move.interact_with_object(2436, 'z', 1, True, pre_interact=click_key, custom_exit_function=get_plans)
    osrs.move.interact_with_object(16679, 'z', 0, False, timeout=6)
    osrs.move.go_to_loc(2465, 3489)
    osrs.move.interact_with_object(1967, 'y', 3492, True)
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=4)
    osrs.move.go_to_loc(2449, 3483, 1)
    quest_items = [
        osrs.item_ids.ItemIDs.STAFF_OF_AIR.value,
        {
            'id': [
                osrs.item_ids.ItemIDs.FIRE_RUNE.value
            ],
            'quantity': 'All'
        },
        {
            'id': [
                osrs.item_ids.ItemIDs.MIND_RUNE.value,
            ],
            'quantity': 'All'
        }
    ]
    osrs.bank.banking_handler({
        'dump_inv': False,
        'dump_equipment': False,
        'search': [{'query': '', 'items': quest_items}]
    })
    osrs.move.go_to_loc(2465, 3498, 1)
    osrs.move.interact_with_object(16684, 'z', 0, False, timeout=6, obj_dist=7, right_click_option='Climb-down')
    osrs.move.interact_with_object(1967, 'y', 3491, False)
    osrs.move.go_to_loc(2474, 3459)
    osrs.move.interact_with_object(16683, 'z', 1, True, timeout=6, obj_dist=7)
    osrs.move.interact_with_object(2447, 'z', 2, True, timeout=6)
    pyautogui.scroll(15)
    osrs.move.interact_with_object(2440, 'z', 2, True, pre_interact=click_t, custom_exit_function=place_t, timeout=5)
    osrs.move.interact_with_object(2441, 'z', 2, True, pre_interact=click_u, custom_exit_function=place_u, timeout=5)
    osrs.move.interact_with_object(2442, 'z', 2, True, pre_interact=click_z, custom_exit_function=place_z, timeout=5)
    osrs.move.interact_with_object(2443, 'z', 2, True, pre_interact=click_o, custom_exit_function=place_o, timeout=5)
    pyautogui.scroll(-50)
    util_functions.equip_staff_and_set_autocast(osrs.item_ids.ItemIDs.STAFF_OF_AIR.value, '201,1,4')
    osrs.player.toggle_run('on')
    osrs.move.interact_with_object(2444, 'x', 5500, True, timeout=8, obj_type='ground')
    util_functions.talk_to_npc('dummy')
    util_functions.dialogue_handler()
    run_to_safe_spot_with_anchor(3)
    osrs.clock.random_sleep(5, 5.1)
    kill_demon()
    run_to_safe_spot(0.1, 2464, 9863)
    run_to_safe_spot(0.1, 2451, 9860)
    run_to_safe_spot(0.1, 2455, 9871)
    osrs.player.toggle_run('off')
    run_to_safe_spot(0.1, 2467, 9884)
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('dummy')
    util_functions.dialogue_handler(dialogue)
    click_roots()
    osrs.move.run_towards_square_v2({'x': 2472, 'y': 9893, 'z': 0})
    util_functions.talk_to_npc('king narnode shareen', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()