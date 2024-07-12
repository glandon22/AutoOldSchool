import osrs
import util_functions
import transport_functions

dialogue = [
    "Can I help at all?",
    "I would be glad to help.",
    "Yes.",
    "Ok, I'll gather some wood.",
    "I'll try my best.",
    "0001",
    "0002",
    "0003",
    "0004",
    "I will find the warlord and bring back the orbs."
]


def wait_for_chat():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({util_functions.main_chat_widget})
    qh.query_backend()
    if qh.get_widgets(util_functions.main_chat_widget):
        return True


def wait_for_orb1():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.ORB_OF_PROTECTION.value):
        return True


def wait_for_orbs_of_protection():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.ORBS_OF_PROTECTION.value):
        return True


def main():
    util_functions.talk_to_npc('king bolren', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2529, 3202, right_click=True)
    util_functions.talk_to_npc('commander montai', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('commander montai', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('commander montai', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2495, 3260, right_click=True)
    util_functions.talk_to_npc('tracker gnome 1', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2526, 3252, right_click=True)
    osrs.move.interact_with_object(1535, 'y', 3255, True, intermediate_tile='2524,3256,0', obj_type='wall')
    util_functions.talk_to_npc('tracker gnome 2', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2495, 3235, right_click=True)
    util_functions.talk_to_npc('tracker gnome 3', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2507, 3210, right_click=True)
    osrs.move.interact_with_object(2181, 'z', 1, True, custom_exit_function=wait_for_chat)
    util_functions.dialogue_handler(["0001"])
    osrs.move.interact_with_object(2181, 'z', 1, True, custom_exit_function=wait_for_chat)
    util_functions.dialogue_handler(["0002"])
    osrs.move.interact_with_object(2181, 'z', 1, True, custom_exit_function=wait_for_chat)
    util_functions.dialogue_handler(["0003"])
    osrs.move.interact_with_object(2181, 'z', 1, True, custom_exit_function=wait_for_chat)
    util_functions.dialogue_handler(["0004"])
    # need to pray melee here
    osrs.move.go_to_loc(2502, 3248, right_click=True)
    osrs.player.toggle_run('on')
    osrs.move.interact_with_object(2185, 'y', 3254, True, custom_exit_function=util_functions.check_for_dialogue)
    util_functions.dialogue_handler([])
    osrs.clock.sleep_one_tick()
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.move.interact_with_object(1535, 'x', 2504, False, obj_dist=7, intermediate_tile='2503,3256,0')
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.move.interact_with_object(16683, 'z', 1, True, obj_dist=7, right_click_option='Climb-up', timeout=4)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.move.interact_with_object(2183, 'z', 1, True, obj_dist=7, custom_exit_function=wait_for_orb1)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.move.interact_with_object(16679, 'z', 0, False, obj_dist=7, right_click_option='Climb-down', timeout=4)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.move.interact_with_object(2184, 'y', 3250, False, intermediate_tile='2502,3249,0', obj_type='wall')
    osrs.player.turn_off_all_prayers()
    osrs.player.toggle_run('off')
    osrs.move.go_to_loc(2501, 3192, right_click=True)
    util_functions.talk_to_npc('elkoy')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2186, 'y', 3161, True, obj_type='wall', timeout=5,
                                   right_click_option='Squeeze-through')
    osrs.move.go_to_loc(2536, 3166, right_click=True)
    util_functions.talk_to_npc('king bolren', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.clock.random_sleep(3, 3.1)
    util_functions.equip_staff_and_set_autocast(osrs.item_ids.ItemIDs.STAFF_OF_AIR.value, '201,1,4')
    osrs.player.toggle_run('on')
    osrs.move.go_to_loc(2457, 3297, right_click=True)
    osrs.combat_utils.pot_handler(None, {})
    osrs.combat_utils.prayer_handler(None, ['protect_melee'])
    osrs.player.toggle_run('off')
    util_functions.talk_to_npc('khazard warlord')
    util_functions.dialogue_handler(dialogue)
    util_functions.kill_single_npc('khazard warlord', ['protect_melee'], {})
    osrs.move.interact_with_object(
        osrs.item_ids.ItemIDs.ORBS_OF_PROTECTION.value, 'x', 1, True,
        obj_type='ground_items', custom_exit_function=wait_for_orbs_of_protection)
    osrs.player.turn_off_all_prayers()
    osrs.player.toggle_run('on')
    osrs.move.go_to_loc(2501, 3192, right_click=True)
    osrs.player.toggle_run('off')
    util_functions.talk_to_npc('elkoy')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(2186, 'y', 3161, True, obj_type='wall', timeout=5,
                                   right_click_option='Squeeze-through')
    osrs.player.toggle_run('off')
    osrs.move.go_to_loc(2536, 3166, right_click=True)
    util_functions.talk_to_npc('king bolren', right_click=True)
    util_functions.dialogue_handler(dialogue, timeout=30)
    util_functions.wait_for_quest_complete_screen()
