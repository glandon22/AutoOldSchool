import osrs
import util_functions
import transport_functions

dialogue = [
    "Yes.",
    "Why can't you sleep, what's wrong?",
    "Can I help at all?",
    "Is there anything else I can help with?",
    "Who's Brother Cedric?",
    "Where should I look?",
    "Yes, I'd be happy to!"
]

def wait_for_blanket():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.ItemIDs.CHILDS_BLANKET.value):
        return True


def main():
    util_functions.talk_to_npc('brother omad', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2560, 3220)
    osrs.move.interact_with_object(16680, 'y', 5500, True, right_click_option='Climb-down', timeout=5)
    osrs.player.toggle_run('on')
    osrs.move.interact_with_object(1535, 'y', 9612, False, intermediate_tile='2565,9610,0', obj_type='wall')
    osrs.move.go_to_loc(2566, 9605, right_click=True)
    osrs.move.interact_with_object(
        595, 'y',
        9612, False, obj_type='game',
        custom_exit_function=wait_for_blanket
    )
    osrs.move.go_to_loc(2565, 9611)
    osrs.move.interact_with_object(17385, 'y', 5500, False, right_click_option='Climb-up', timeout=5)
    osrs.player.toggle_run('off')
    osrs.move.go_to_loc(2606, 3220)
    util_functions.talk_to_npc('brother omad', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('brother omad', right_click=True)
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2621, 3257)
    util_functions.talk_to_npc('brother cedric')
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('brother cedric')
    util_functions.dialogue_handler(dialogue)
    util_functions.talk_to_npc('brother cedric')
    util_functions.dialogue_handler(dialogue)
    osrs.move.go_to_loc(2606, 3213)
    util_functions.talk_to_npc('brother omad', right_click=True)
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()