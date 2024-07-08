import transport_functions
import util_functions

dialogue = [
    "Have you any quests for me?",
    "Yes.",
    "I'm looking for the head wizard.",
    "Okay, here you are.",
    "Yes, certainly.",
    "I've been sent here with a package for you.",
    "Go ahead."
]

def main():
    util_functions.talk_to_npc('duke horacio')
    util_functions.dialogue_handler(dialogue)
    transport_functions.necklace_of_passage_tele_wiz_tower()
    transport_functions.walk_to_loc(3107, 3112, 3167, 3171, 3109, 3168)
    util_functions.walk_through_door(23972, 'y', 3166, False, 5, '3109,3164,0')
    util_functions.walk_through_door(23972, 'x', 3104, False, 5, '3102,3163,0', door_type='game')
    util_functions.walk_through_door(2147, 'y', 5600, True, 5, door_type='game', timeout=3)
    util_functions.walk_through_door(1535, 'x', 3098, False, 8, '3097,9570,0')
    util_functions.talk_to_npc('archmage sedridor')
    util_functions.dialogue_handler(dialogue)
    util_functions.tab_to_varrock()
    transport_functions.walk_to_loc(3250, 3254, 3395, 3398, 3251, 3397)
    util_functions.talk_to_npc('aubury', right_click=True)
    util_functions.dialogue_handler(dialogue)
    transport_functions.necklace_of_passage_tele_wiz_tower()
    transport_functions.walk_to_loc(3107, 3112, 3167, 3171, 3109, 3168)
    util_functions.walk_through_door(23972, 'y', 3166, False, 5, '3109,3164,0')
    util_functions.walk_through_door(23972, 'x', 3104, False, 5, '3102,3163,0', door_type='game')
    util_functions.walk_through_door(2147, 'y', 5600, True, 5, door_type='game', timeout=3)
    util_functions.walk_through_door(1535, 'x', 3098, False, 8, '3097,9570,0')
    util_functions.talk_to_npc('archmage sedridor')
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()