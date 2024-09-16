import datetime

import osrs
import transport_functions
import util_functions

dialogue = [
    "And how is life as a squire?",
    "Yes.",
    "I can make a new sword if you like...",
    "So would these dwarves make another one?",
    "Ok, I'll give it a go.",
    "What do you know about the Imcando dwarves?",
    "Would you like a redberry pie?",
    "Can you make a special sword for me?",
    "About that sword...",
    "Can you make that replacement sword now?"
]


def find_world_with_no_vyin():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['sir vyvin'])
    while True:
        qh.query_backend()
        if qh.get_npcs_by_name() and qh.get_npcs_by_name()[0]['y_coord'] >= 3337:
            return
        else:
            osrs.game.hop_worlds(total_level_worlds=False)


def wait_for_open():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {2272})
    qh.query_backend()
    if qh.get_objects_v2('game', 2272):
        return True


def wait_for_pic():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.PORTRAIT):
        return True


def mine_rock():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    osrs.move.go_to_loc(3049, 9567)
    qh.set_objects_v2('game', {11378})
    last_rock_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.combat_utils.prayer_handler(None, ['protect_melee'])
        osrs.combat_utils.pot_handler(None, {})
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.BLURITE_ORE):
            return
        elif qh.get_objects_v2('game', 11378) and (datetime.datetime.now() - last_rock_click).total_seconds() > 30:
            rocks = sorted(qh.get_objects_v2('game', 11378), key=lambda rock: rock['dist'])
            res = osrs.move.right_click_v6(rocks[0], 'Mine', qh.get_canvas(), in_inv=True)
            if res:
                last_rock_click = datetime.datetime.now()

def main():
    util_functions.talk_to_npc('squire', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.tab_to_varrock()
    osrs.move.go_to_loc(3210, 3488, right_click=True)
    osrs.move.interact_with_object(11773, 'y', 3490, True, obj_type='wall', intermediate_tile='3209,3493,0',
                                   obj_tile={'x': 3210, 'y': 3490})
    util_functions.talk_to_npc('reldo', right_click=True)
    util_functions.dialogue_handler(dialogue)
    transport_functions.tab_to_fally()
    osrs.move.go_to_loc(2994, 3144)
    util_functions.talk_to_npc('thurgo')
    util_functions.dialogue_handler(dialogue)
    transport_functions.tab_to_fally()
    osrs.move.go_to_loc(2970, 3341, right_click=True)
    util_functions.talk_to_npc('squire', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        24059, 'x', 2982, True,
        intermediate_tile='2984,3341,0', obj_type='wall', obj_tile={'x': 2981, 'y': 3341}
    )
    osrs.move.interact_with_object(
        24057, 'x', 2986, True, intermediate_tile='2988,3341,0',
        obj_type='wall', obj_tile={'x': 2985, 'y': 3341}
    )
    osrs.move.interact_with_object(
        24057, 'x', 2992, True, intermediate_tile='2995,3343,0',
        obj_type='wall', obj_tile={'x': 2991, 'y': 3341}
    )
    osrs.move.interact_with_object(24070, 'z', 1, True, timeout=4, right_click_option='Climb-up', obj_dist=5)
    osrs.move.interact_with_object(
        24057, 'x', 2990, False, intermediate_tile='2989,3341,1',
        obj_type='wall', obj_tile={'x': 2991, 'y': 3341}
    )
    osrs.move.interact_with_object(24077, 'z', 2, True, timeout=4, right_click_option='Climb-up', obj_dist=8)
    osrs.move.interact_with_object(
        24057, 'y', 3336, False, intermediate_tile='2982,3332,2',
        obj_type='wall', obj_tile={'x': 2982, 'y': 3337}
    )
    find_world_with_no_vyin()
    osrs.move.interact_with_object(2271, 'x', 9999, True, custom_exit_function=wait_for_open)
    osrs.move.interact_with_object(2272, 'x', 9999, True, custom_exit_function=util_functions.check_for_dialogue)
    util_functions.dialogue_handler([])
    transport_functions.tab_to_fally()
    osrs.move.go_to_loc(2994, 3144)
    util_functions.talk_to_npc('thurgo')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(1738, 'y', 5500, True, timeout=8, right_click_option='Climb-down')
    # mine the ore, need to pray melee and check to drink pot if needed
    osrs.player.toggle_run('on')
    osrs.move.go_to_loc(3019, 9581)
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.combat_utils.pot_handler(None, {})
    mine_rock()
    osrs.move.go_to_loc(3002, 9548)
    osrs.player.turn_off_all_prayers()
    osrs.player.toggle_run('off')
    osrs.move.interact_with_object(17385, 'y', 5500, False, timeout=5, right_click_option='Climb-up')
    util_functions.talk_to_npc('thurgo')
    util_functions.dialogue_handler(dialogue)
    transport_functions.tab_to_fally()
    osrs.move.go_to_loc(2970, 3341, right_click=True)
    util_functions.talk_to_npc('squire', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()