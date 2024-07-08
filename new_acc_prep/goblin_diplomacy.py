import osrs
import transport_functions
import util_functions

quest_dialogue = [
    "So how is life for the goblins?",
    "Yes.",
    "Yes, Wartface looks fat",
    "Do you want me to pick an armour colour for you?",
    "What about a different colour?",
    "I have some orange armour here.",
    "I have some blue armour here.",
    "I have some brown armour here.",
    "Okay, I'll be back soon.",
    "Yes, he looks fat."
]

def main():
    transport_functions.enter_goblin_hall()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.dye_goblin_mail()
    transport_functions.enter_goblin_hall()
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.enter_goblin_hall()
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.enter_goblin_hall()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.wait_for_quest_complete_screen()