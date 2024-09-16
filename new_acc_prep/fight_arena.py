import datetime

import osrs
import util_functions
import transport_functions

dialogue = [
    "Can I help you?",
    "Yes.",
    "I'd like a Khali brew please.",
]


def in_bar():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2563 <= qh.get_player_world_location('x') <= 2570 and 3139 <= qh.get_player_world_location('y') <= 3150:
        return True


def click_keys():
    util_functions.equip_item(osrs.item_ids.KHAZARD_CELL_KEYS)


def get_to_safe_spot():
    corpse = 662
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects_v2('game', {corpse})
    time_on_tile = datetime.datetime.now()
    corpse_data = None
    while True:
        osrs.combat_utils.prayer_handler(None, ['protect_melee'])
        osrs.combat_utils.pot_handler(None, {})
        osrs.player.toggle_run('on')
        qh.query_backend()
        if qh.get_objects_v2('game', corpse):
            if not corpse_data:
                corpse_data = sorted(qh.get_objects_v2('game', corpse), key=lambda obj: obj['dist'], reverse=True)[0]
            targ_tile = f'{corpse_data["x_coord"] - 1},{corpse_data["y_coord"]},0'
            qh.set_tiles({targ_tile})
            if qh.get_player_world_location('x') == corpse_data['x_coord'] - 1 and qh.get_player_world_location('y') == corpse_data['y_coord']:
                if (datetime.datetime.now() - time_on_tile).total_seconds() > 2.4:
                    osrs.player.turn_off_all_prayers()
                    osrs.clock.sleep_one_tick()
                    return
            else:
                time_on_tile = datetime.datetime.now()

            if qh.get_tiles(targ_tile):
                osrs.move.fast_click(qh.get_tiles(targ_tile))


def main():
    util_functions.talk_to_npc('lady servil')
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2613, 3188, right_click=True)
    osrs.move.interact_with_object(1535, 'y', 3191, True, obj_type='wall', intermediate_tile='2611,3193,0',
                                   obj_tile={'x': 2609, 'y': 3191})
    osrs.move.interact_with_object(
        75, 'x', 1, False,
        custom_exit_function=util_functions.check_for_item_in_inv,
        custom_exit_function_arg=osrs.item_ids.KHAZARD_HELMET
    )
    osrs.move.interact_with_object(1535, 'y', 3188, False, obj_type='wall', intermediate_tile='2609,3188,0',
                                   obj_tile={'x': 2609, 'y': 3191})
    osrs.move.go_to_loc(2617, 3173)
    util_functions.equip_item(osrs.item_ids.KHAZARD_HELMET)
    util_functions.equip_item(osrs.item_ids.KHAZARD_ARMOUR)
    osrs.move.interact_with_object(81, 'y', 3171, False, obj_type='wall')
    osrs.move.go_to_loc(2616, 3150, right_click=True)
    osrs.move.interact_with_object(1540, 'y', 3146, False, obj_type='wall', intermediate_tile='2616,3144,0')
    util_functions.talk_to_npc('head guard')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(1535, 'x', 2608, False, obj_type='wall', intermediate_tile='2606,3141,0',
                                   obj_tile={'x': 2609, 'y': 3143})
    osrs.move.go_to_loc(2587, 3140, right_click=True)
    osrs.move.interact_with_object(81, 'x', 2584, False, obj_type='wall', obj_dist=7)
    osrs.move.go_to_loc(2570, 3152)
    osrs.move.interact_with_object(
        1535, 'x', 1, False, obj_type='wall',
        intermediate_tile='2568,3146,0', obj_tile={'x': 2569, 'y': 3150}, custom_exit_function=in_bar
    )
    osrs.move.go_to_loc(2566, 3142)
    util_functions.talk_to_npc('khazard barman', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        1535, 'x', 2569, True, obj_type='wall',
        intermediate_tile='2577,3150,0', obj_tile={'x': 2569, 'y': 3150}
    )
    osrs.move.go_to_loc(2584, 3141)
    osrs.move.go_to_loc(2602, 3140, right_click=True)
    osrs.move.interact_with_object(1535, 'x', 2609, True, obj_type='wall', intermediate_tile='2611,3141,0',
                                   obj_tile={'x': 2609, 'y': 3143})
    util_functions.talk_to_npc('head guard', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(1540, 'y', 3147, True, obj_type='wall', intermediate_tile='2619,3147,0')
    osrs.move.go_to_loc(2619, 3165, right_click=True)
    osrs.move.interact_with_object(
        80, 'x', 2616, False, obj_type='wall',
        custom_exit_function=util_functions.check_for_dialogue,
        right_click_option='Use',
        pre_interact=click_keys
    )
    util_functions.dialogue_handler(dialogue)
    get_to_safe_spot()
    util_functions.kill_single_npc('khazard ogre', [], {})
    osrs.clock.random_sleep(10, 10.1)
    util_functions.dialogue_handler(dialogue)
    get_to_safe_spot()
    util_functions.kill_single_npc('khazard scorpion', [], {})
    osrs.clock.random_sleep(5, 5.1)
    util_functions.dialogue_handler(dialogue)
    get_to_safe_spot()
    util_functions.kill_single_npc('bouncer', ['protect_melee'], {})
    # died right after this so did not get to properly test FYI
    osrs.clock.random_sleep(5, 5.1)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(46563, 'x', 5000, False, right_click_option='Quick-escape')
    osrs.move.interact_with_object(82, 'x', 9999, True, custom_exit_function=util_functions.check_for_dialogue, right_click_option='Open')
    util_functions.dialogue_handler(dialogue, timeout=1)
    osrs.move.interact_with_object(46563, 'x', 5000, False, right_click_option='Quick-escape')
    osrs.player.toggle_run('off')
    osrs.move.interact_with_object(
        1535, 'x', 2613, True, obj_type='wall',
        obj_tile={'x': 2613, 'y': 3150}, intermediate_tile='2618,3157,0', right_click_option='Open'
    )
    osrs.move.go_to_loc(2618, 3170)
    osrs.move.interact_with_object(81, 'y', 3172, True, obj_type='wall')
    osrs.move.go_to_loc(2565, 3201)
    util_functions.talk_to_npc('lady servil')
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()