import osrs
import util_functions
import transport_functions
main_chat_widget = '162,34'


quest_dialogue = [
    "Yes, I have seen her actually!",
    "Yes, ok, I'll let her know.",
    "Ok, thanks.",
    "Talk about something else.",
    "Talk about Romeo & Juliet.",
    "Yes.",
    "Ok, thanks."
]

def main():
    util_functions.talk_to_npc('romeo', right_click=True)
    util_functions.dialogue_handler(quest_dialogue)
    osrs.move.go_to_loc(3166,3433)
    osrs.move.interact_with_object(
        11773, 'x', 3164, False,
        obj_type='wall', intermediate_tile='3162,3433,0', obj_tile={'x': 3165, 'y': 3433}
    )
    osrs.move.interact_with_object(
        11797, 'z', 1, True, right_click_option='Climb-up'
    )
    osrs.move.interact_with_object(
        11773, 'y', 3430, False,
        obj_type='wall', intermediate_tile='3156,3428,1', obj_tile={'x': 3157, 'y': 3430}
    )
    osrs.move.interact_with_object(
        11773, 'y', 3426, False,
        obj_type='wall', intermediate_tile='3156,3425,1', obj_tile={'x': 3158, 'y': 3426}
    )
    util_functions.talk_to_npc('juliet')
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.tab_to_varrock()
    util_functions.talk_to_npc('romeo', right_click=True)
    util_functions.dialogue_handler(quest_dialogue)
    osrs.move.go_to_loc(3248, 3479)
    util_functions.talk_to_npc('father lawrence')
    util_functions.dialogue_handler(quest_dialogue)
    osrs.move.go_to_loc(3190, 3403),
    util_functions.talk_to_npc('apothecary')
    util_functions.dialogue_handler(quest_dialogue)
    osrs.move.go_to_loc(3166, 3433)
    osrs.move.interact_with_object(
        11773, 'x', 3164, False,
        obj_type='wall', intermediate_tile='3162,3433,0', obj_tile={'x': 3165, 'y': 3433}
    )
    osrs.move.interact_with_object(
        11797, 'z', 1, True, right_click_option='Climb-up'
    )
    osrs.move.interact_with_object(
        11773, 'y', 3430, False,
        obj_type='wall', intermediate_tile='3156,3428,1', obj_tile={'x': 3157, 'y': 3430}
    )
    osrs.move.interact_with_object(
        11773, 'y', 3426, False,
        obj_type='wall', intermediate_tile='3156,3425,1', obj_tile={'x': 3158, 'y': 3426}
    )
    util_functions.talk_to_npc('juliet')
    util_functions.dialogue_handler(quest_dialogue, timeout=15)
    util_functions.tab_to_varrock()
    util_functions.talk_to_npc('romeo', right_click=True)
    util_functions.dialogue_handler(quest_dialogue, timeout=60)
    util_functions.wait_for_quest_complete_screen()

