import datetime

import osrs.clock
import util_functions
import transport_functions

dialogue = [
    "How can I help?",
    "Yes."
]


def rope_to_rock():
    rock = 1996
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_objects_v2('game', {rock})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if (qh.get_player_world_location('y') >= 3475
                and qh.get_objects_v2('game', rock)
                and qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value)):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value))
            osrs.move.fast_click(qh.get_objects_v2('game', rock)[0])
        elif qh.get_player_world_location('y') <= 3468:
            return


def rope_to_tree():
    rock = 2020
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_objects_v2('game', {rock})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if (qh.get_player_world_location('y') >= 3465
                and qh.get_objects_v2('game', rock)
                and qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value)):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.ROPE.value))
            osrs.move.fast_click(qh.get_objects_v2('game', rock)[0])
        elif qh.get_player_world_location('y') <= 3463:
            return


def read_book():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.BOOK_ON_BAXTORIAN.value):
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.BOOK_ON_BAXTORIAN.value))
            osrs.clock.random_sleep(1, 1.1)
            osrs.keeb.press_key('esc')
            return


# dax walker doesnt work in c wars for whatever reason
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


def wait_for_key():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.KEY_293.value):
        return True
    return False


def wait_for_ammy():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value):
        return True
    return False


def wait_for_urn():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_URN.value):
        return True
    return False


def wait_for_key_final():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.KEY_298.value):
        return True
    return False


def click_glarials_pebble():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_PEBBLE.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_PEBBLE.value))


def click_air():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.AIR_RUNE.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.AIR_RUNE.value))


def click_water():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value))


def click_earth():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.EARTH_RUNE.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.EARTH_RUNE.value))


def walk_to_tile(tile):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({f'{tile["x"]},{tile["y"]},0'})
    qh.set_player_world_location()
    time_on_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') == tile['x'] and qh.get_player_world_location('y') == tile['y']:
            if (datetime.datetime.now() - time_on_tile).total_seconds() > 3:
                return
        else:
            time_on_tile = datetime.datetime.now()

        if (qh.get_tiles(f'{tile["x"]},{tile["y"]},0')
                and not (qh.get_player_world_location('x') == tile['x'] and qh.get_player_world_location('y') == tile[
                    'y'])):
            osrs.move.fast_click(qh.get_tiles(f'{tile["x"]},{tile["y"]},0'))


def use_air_rune(quantity):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.AIR_RUNE.value):
        if qh.get_inventory(osrs.item_ids.ItemIDs.AIR_RUNE.value)['quantity'] == quantity:
            return True
    elif quantity == 0 and not qh.get_inventory(osrs.item_ids.ItemIDs.AIR_RUNE.value):
        return True


def use_water_rune(quantity):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value):
        if qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value)['quantity'] == quantity:
            return True
    elif quantity == 0 and not qh.get_inventory(osrs.item_ids.ItemIDs.WATER_RUNE.value):
        return True


def use_earth_rune(quantity):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.EARTH_RUNE.value):
        if qh.get_inventory(osrs.item_ids.ItemIDs.EARTH_RUNE.value)['quantity'] == quantity:
            return True
    elif quantity == 0 and not qh.get_inventory(osrs.item_ids.ItemIDs.EARTH_RUNE.value):
        return True


def remove_amulet():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({'387,17'})
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value):
            return True
        elif qh.get_widgets('387,17'):
            osrs.move.click(qh.get_widgets('387,17'))
            osrs.keeb.press_key('esc')
            osrs.clock.sleep_one_tick()
        else:
            osrs.keeb.press_key('f4')
            osrs.clock.sleep_one_tick()


def consume_amulet():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory() and not qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value):
        return True


def empty_urn():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({util_functions.main_chat_widget})
    qh.query_backend()
    if qh.get_widgets(util_functions.main_chat_widget):
        return True


def right_click_amulet():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value):
        osrs.move.right_click_v6(
            qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value), 'Use', qh.get_canvas(), in_inv=True
        )


def click_urn():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_URN.value):
        osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.GLARIALS_URN.value))


def main():
    util_functions.walk_through_door(
        1560, 'x', 2527, False, intermediate_tile='2525,3495,0', door_dist=5
    )
    util_functions.walk_through_door(
        1540, 'x', 2524, False, intermediate_tile='2522,3495,0'
    )
    util_functions.talk_to_npc('almera')
    util_functions.dialogue_handler(dialogue)
    util_functions.walk_through_door(
        1560, 'x', 2512, False, intermediate_tile='2511,3495,0'
    )
    util_functions.walk_through_door(
        1987, 'y', 3481, False, door_type='game'
    )
    osrs.clock.random_sleep(2, 2.1)
    util_functions.talk_to_npc('hudon')
    util_functions.dialogue_handler(dialogue)
    transport_functions.walk_to_loc(2511, 2513, 3476, 3478, 2512, 3477)
    rope_to_rock()
    rope_to_tree()
    util_functions.walk_through_door(
        2022, 'y', 3460, False, door_type='game', door_dist=5
    )
    transport_functions.walk_to_loc(2523, 2525, 3432, 3434, 2524, 3433)
    util_functions.walk_through_door(
        1543, 'x', 2520, False, door_dist=5, intermediate_tile='2519,3432,0'
    )
    util_functions.walk_through_door(
        16671, 'z', 1, True, door_type='game', door_dist=5, timeout=4
    )
    util_functions.walk_through_door(
        1989, 'y', 3427, False, door_type='game'
    )
    read_book()
    transport_functions.dueling_to_c_wars()
    walk_out_of_c_wars()
    transport_functions.walk_to_loc(2530, 2535, 3154, 3156, 2531, 3155)
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.player.toggle_run('on')
    util_functions.walk_through_door(
        5250, 'y', 5500, True, door_type='game', door_dist=5, timeout=3
    )
    util_functions.interact_with_object(1990, 'x', 1, True, door_type='game', custom_exit_function=wait_for_key)
    transport_functions.walk_to_loc(2514, 2516, 9566, 9570, 2515, 9568)
    util_functions.interact_with_object(1991, 'y', 9576, True)
    osrs.player.turn_off_all_prayers()
    util_functions.talk_to_npc('golrie')
    util_functions.dialogue_handler(dialogue)
    util_functions.interact_with_object(1991, 'y', 9575, False)
    transport_functions.walk_to_loc(2530, 2536, 9548, 9556, 2533, 9552)
    util_functions.interact_with_object(17387, 'y', 5500, False, door_type='game', timeout=4)
    osrs.player.turn_off_all_prayers()
    osrs.player.toggle_run('off')
    transport_functions.games_neck_to_barb()
    transport_functions.walk_to_loc(2554, 2560, 3441, 3449, 2555, 3444)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.player.toggle_run('on')
    util_functions.interact_with_object(1992, 'y', 5500, True, door_type='game', pre_interact=click_glarials_pebble)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    transport_functions.walk_to_loc(2538, 2540, 9842, 9845, 2539, 9844)
    # may need to turn right click to atk monsters on bc they can block the chest
    util_functions.interact_with_object(1994, 'y', 5500, True, door_type='game', custom_exit_function=wait_for_ammy)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    transport_functions.walk_to_loc(2538, 2543, 9815, 9821, 2541, 9818)
    util_functions.interact_with_object(1993, 'y', 5500, True, door_type='game', custom_exit_function=wait_for_urn)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    transport_functions.walk_to_loc(2550, 2555, 9840, 9846, 2551, 9844)
    util_functions.interact_with_object(17387, 'y', 5500, False, door_type='game', timeout=4)
    osrs.player.toggle_run('off')
    osrs.player.turn_off_all_prayers()
    transport_functions.games_neck_to_barb()
    quest_items = [
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.AIR_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.EARTH_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.WATER_RUNE.value,
        osrs.item_ids.ItemIDs.GLARIALS_AMULET.value,
        osrs.item_ids.ItemIDs.GLARIALS_URN.value,
        osrs.item_ids.ItemIDs.ROPE.value,
        osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
        osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
        {
            'id': [
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE5.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE4.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE3.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE2.value,
                osrs.item_ids.ItemIDs.NECKLACE_OF_PASSAGE1.value,
            ],
            'quantity': '1'
        },
    ]
    osrs.bank.banking_handler({
        'dump_inv': True,
        'dump_equipment': True,
        'search': [{'query': '', 'items': quest_items}]
    })
    util_functions.equip_item(osrs.item_ids.ItemIDs.GLARIALS_AMULET.value)
    transport_functions.walk_to_loc(2528, 2530, 3494, 3497, 2529, 3495)
    util_functions.walk_through_door(
        1560, 'x', 2527, False, intermediate_tile='2525,3495,0', door_dist=5
    )
    util_functions.walk_through_door(
        1540, 'x', 2524, False, intermediate_tile='2522,3495,0'
    )
    util_functions.walk_through_door(
        1560, 'x', 2512, False, intermediate_tile='2511,3495,0'
    )
    util_functions.walk_through_door(
        1987, 'y', 3481, False, door_type='game'
    )
    osrs.clock.random_sleep(2, 2.1)
    transport_functions.walk_to_loc(2511, 2513, 3476, 3478, 2512, 3477)
    rope_to_rock()
    rope_to_tree()
    util_functions.interact_with_object(2010, 'y', 5500, True, door_type='game')
    osrs.player.toggle_run('on')
    util_functions.interact_with_object(
        1524, 'x', 2582, True, obj_tile={'x': 2582, 'y': 9876}, intermediate_tile='2590,9883,0'
    )
    util_functions.interact_with_object(
        1999, 'x', 2582, True, custom_exit_function=wait_for_key_final, door_type='game'
    )
    transport_functions.walk_to_loc(2563, 2565, 9877, 9879, 2564, 9878)
    util_functions.equip_item(osrs.item_ids.ItemIDs.PRAYER_POTION4.value)
    osrs.clock.sleep_one_tick()
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    util_functions.interact_with_object(
        1524, 'y', 9882, True, obj_tile={'x': 2565, 'y': 9881}, intermediate_tile='2565,9886,0'
    )
    util_functions.interact_with_object(
        2002, 'y', 9894, True, intermediate_tile='2568,9897,0', obj_tile={'x': 2568, 'y': 9893}
    )
    util_functions.interact_with_object(
        2002, 'y', 9902, True, intermediate_tile='2566,9905,0', obj_tile={'x': 2566, 'y': 9901}
    )
    osrs.player.turn_off_all_prayers()
    osrs.player.toggle_run('off')
    walk_to_tile({'x': 2563, 'y': 9910})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9910}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=5
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9910}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=5
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9910}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=5
    )
    # pillar 2
    walk_to_tile({'x': 2563, 'y': 9912})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9912}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=4
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9912}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=4
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9912}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=4
    )
    # pillar 3
    walk_to_tile({'x': 2563, 'y': 9914})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9914}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=3
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9914}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=3
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2562, 'y': 9914}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=3
    )
    # pillar 4
    walk_to_tile({'x': 2568, 'y': 9914})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9914}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=2
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9914}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=2
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9914}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=2
    )
    # pillar 5
    walk_to_tile({'x': 2568, 'y': 9912})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9912}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=1
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9912}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=1
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9912}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=1
    )
    # pillar 6
    walk_to_tile({'x': 2568, 'y': 9910})
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9910}, timeout=3, pre_interact=click_air,
        custom_exit_function=use_air_rune, custom_exit_function_arg=0
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9910}, timeout=3, pre_interact=click_earth,
        custom_exit_function=use_earth_rune, custom_exit_function_arg=0
    )
    util_functions.interact_with_object(
        2005, 'y', 9902, True,
        door_type='game', obj_tile={'x': 2569, 'y': 9910}, timeout=3, pre_interact=click_water,
        custom_exit_function=use_water_rune, custom_exit_function_arg=0
    )
    remove_amulet()
    util_functions.interact_with_object(
        2006, 'x', 1, True, door_type='game',
        custom_exit_function=consume_amulet, pre_interact=right_click_amulet
    )
    util_functions.interact_with_object(
        2014, 'x', 1, True, door_type='game',
        custom_exit_function=empty_urn, pre_interact=click_urn, timeout=12
    )
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()