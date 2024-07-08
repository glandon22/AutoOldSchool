import osrs
import transport_functions
import util_functions

dialogue = [
"I'm in search of a quest.", "Okay, I will try and help.",
"I've been sent to help purify the Varrock stone circle.",
"Ok, I'll do that then.",
    "Yes.",

]


def open_first_door():
    door_id = 1535
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    qh.set_tiles({'2896,3428,0'})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2895:
            break
        elif qh.get_objects_v2('wall', door_id, 3):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id, 3)[0])
        elif qh.get_tiles('2896,3428,0'):
            osrs.move.fast_click(qh.get_tiles('2896,3428,0'))


def go_up_stairs():
    stairs = 16671
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {stairs})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 1:
            break
        elif qh.get_objects_v2('game', stairs):
            osrs.move.fast_click(qh.get_objects_v2('game', stairs)[0])


def go_down_stairs():
    stairs = 16673
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {stairs})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 0:
            break
        elif qh.get_objects_v2('game', stairs):
            osrs.move.fast_click(qh.get_objects_v2('game', stairs)[0])


def enter_tav_dungeon():
    stairs = 16680
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {stairs})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 5500:
            osrs.player.toggle_run('on')
            break
        elif qh.get_objects_v2('game', stairs):
            osrs.move.fast_click(qh.get_objects_v2('game', stairs)[0])
            osrs.clock.sleep_one_tick()

def main():
    util_functions.talk_to_npc('kaqemeex')
    util_functions.dialogue_handler(dialogue)
    transport_functions.walk_to_loc(2894, 2901, 3425, 3431, 2895, 3428)
    open_first_door()
    go_up_stairs()
    util_functions.talk_to_npc('sanfew')
    util_functions.dialogue_handler(dialogue)
    go_down_stairs()
    transport_functions.walk_to_loc(2882, 2886, 3395, 3401, 2883, 3400)
    enter_tav_dungeon()
    transport_functions.walk_to_loc(2882, 2886, 9829, 9832, 2883, 9830)
    util_functions.enchant_meats()
    util_functions.leave_cauldron()
    transport_functions.walk_to_loc(2894, 2901, 3425, 3431, 2895, 3428)
    open_first_door()
    go_up_stairs()
    util_functions.talk_to_npc('sanfew')
    util_functions.dialogue_handler(dialogue)
    go_down_stairs()
    transport_functions.walk_to_loc(2911, 2915, 3484, 3488, 2913, 3486)
    util_functions.talk_to_npc('kaqemeex')
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()