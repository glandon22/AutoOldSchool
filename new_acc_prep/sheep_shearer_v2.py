import osrs
import util_functions
import transport_functions

dialogue = [
    "I'm looking for a quest.", "Yes, okay. I can do that.", "Yes.",
    "Climb down the stairs.", "I need to talk to you about shearing these sheep!"
]


def main():
    util_functions.talk_to_npc('farmer fred')
    util_functions.dialogue_handler(dialogue)
    util_functions.wait_for_quest_complete_screen()