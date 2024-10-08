import datetime

import osrs
import transport_functions
import util_functions

dialogue = [
    "I suppose so, how do I get there?",
    "Yes.",
    "Will you take me there?",
]

def get_glass():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.BROKEN_GLASS_1469):
        return True


def get_sticks():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.DAMP_STICKS):
        return True


def dry_sticks():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.DRY_STICKS):
            return
        elif qh.get_inventory(osrs.item_ids.DAMP_STICKS) and qh.get_inventory(osrs.item_ids.BROKEN_GLASS_1469):
            osrs.move.click(qh.get_inventory(osrs.item_ids.BROKEN_GLASS_1469))
            osrs.move.click(qh.get_inventory(osrs.item_ids.DAMP_STICKS))
            osrs.clock.random_sleep(3, 3.1)


def click_sticks():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.LIT_TORCH):
            return
        elif qh.get_inventory(osrs.item_ids.DRY_STICKS):
            osrs.move.click(qh.get_inventory(osrs.item_ids.DRY_STICKS))
            osrs.clock.random_sleep(3, 3.1)


def kick_wall():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {18251})
    start = None
    while True:
        qh.query_backend()
        if start and (datetime.datetime.now() - start).total_seconds() > 25:
            return

        if qh.get_objects_v2('game', 18251):
            osrs.move.fast_click(qh.get_objects_v2('game', 18251)[0])
            if not start:
                start = datetime.datetime.now()


def main():
    util_functions.talk_to_npc('caroline')
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('holgart')
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('holgart', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        18324, 'z', 1, True, timeout=7, right_click_option='Climb-up'
    )
    osrs.move.interact_with_object(18168, 'x', 2766, False, intermediate_tile='2764,3283,1', obj_type='wall')
    util_functions.talk_to_npc('kennith', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(18168, 'x', 2767, True, intermediate_tile='2768,3283,1', obj_type='wall')
    osrs.move.interact_with_object(
        18325, 'z', 0, False, timeout=7, right_click_option='Climb-down', intermediate_tile='2780,3283,1'
    )
    osrs.move.go_to_loc(2776, 3281)
    util_functions.talk_to_npc('holgart', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(5, 5.1)
    util_functions.dialogue_handler([])
    util_functions.talk_to_npc('kent')
    util_functions.dialogue_handler(dialogue)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('holgart', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.dialogue_handler([])
    osrs.move.go_to_loc(2769, 3288)
    osrs.move.interact_with_object(
        18168, 'x', 2767, False, intermediate_tile='2765,3288,0',
        obj_type='wall', obj_tile={'x': 2768, 'y': 3288}
    )
    osrs.move.interact_with_object(
        1469, 'x', 2767, False, custom_exit_function=get_glass,
        obj_type='ground_items', obj_tile={'x': 2766, 'y': 3289}
    )
    osrs.move.interact_with_object(
        1467, 'x', 2767, False, custom_exit_function=get_sticks,
        obj_type='ground_items', intermediate_tile='2777,3281,0'
    )
    dry_sticks()
    click_sticks()
    osrs.move.go_to_loc(2782, 3288)
    osrs.move.interact_with_object(18324, 'z', 1, True, timeout=4, right_click_option='Climb-up')
    osrs.move.interact_with_object(18168, 'x', 2766, False, intermediate_tile='2764,3283,1', obj_type='wall')
    util_functions.talk_to_npc('kennith', right_click=True)
    util_functions.dialogue_handler(dialogue)
    kick_wall()
    osrs.move.interact_with_object(18324, 'z', 1, True, timeout=4, right_click_option='Climb-up')
    osrs.move.interact_with_object(18168, 'x', 2766, False, intermediate_tile='2764,3283,1', obj_type='wall')
    util_functions.talk_to_npc('kennith', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(18168, 'x', 2767, True, intermediate_tile='2768,3283,1', obj_type='wall')
    osrs.move.interact_with_object(0, 'y', 3290, True, intermediate_tile='2770,3291,1')
    osrs.move.interact_with_object(18327, 'x', 1, True, custom_exit_function=util_functions.check_for_dialogue)
    util_functions.dialogue_handler([])
    osrs.move.interact_with_object(
        18325, 'z', 0, False, timeout=7, right_click_option='Climb-down', intermediate_tile='2780,3283,1'
    )
    osrs.move.go_to_loc(2776, 3278)
    util_functions.talk_to_npc('holgart', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(5, 5.1)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('caroline', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()