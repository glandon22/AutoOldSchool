import osrs
import util_functions
import transport_functions
main_chat_widget = '162,34'


quest_dialogue = [
    "I wanted to use your anvils.",
    "Yes, I will get you the materials.",
    "Yes.",
]


def main():
    transport_functions.walk_to_loc(2940, 2948, 3449, 3454, 2948, 3451)
    transport_functions.enter_dorics()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.wait_for_quest_complete_screen()