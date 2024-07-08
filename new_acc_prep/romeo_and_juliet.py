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


def start_quest():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['romeo'])
    qh.set_chat_options()
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_npcs_by_name() and (qh.get_widgets(main_chat_widget) and qh.get_widgets(main_chat_widget)['isHidden']):
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            complete = util_functions.dialogue_handler(quest_dialogue)
            if complete:
                return

def main():
    start_quest()
    transport_functions.go_up_to_juliet()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.tab_to_varrock()
    start_quest()
    transport_functions.go_to_father_lawrence()
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.find_and_talk_to_npc('apothecary', 3190, 3403)
    util_functions.dialogue_handler(quest_dialogue)
    transport_functions.go_up_to_juliet()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.wait_for_dialogue()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.tab_to_varrock()
    start_quest()
    util_functions.wait_for_dialogue()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.wait_for_dialogue()
    util_functions.dialogue_handler(quest_dialogue)
    util_functions.wait_for_quest_complete_screen()