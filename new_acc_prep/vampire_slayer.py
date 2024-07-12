import osrs
import util_functions
import transport_functions
main_chat_widget = '162,34'


quest_dialogue = [
    "Ok, I'm up for an adventure.",
    "Accept quest",
    "Yes.",
    "Morgan needs your help!"
]

def main():
    osrs.move.interact_with_object(
        1535, 'y', 3270, False, obj_type='wall',
        obj_tile={'x': 3098, 'y': 3270}, intermediate_tile='3096,3269,0'
    )
    util_functions.talk_to_npc('morgan',right_click=True)
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.tab_to_varrock()
    transport_functions.find_and_talk_to_npc('dr harlow', 3223, 3398)
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.find_and_talk_to_npc('dr harlow', 3223, 3398)
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.glory_to_draynor()
    transport_functions.walk_to_draynor_manor()
    transport_functions.draynor_manor_basement()
    util_functions.kill_vampire()