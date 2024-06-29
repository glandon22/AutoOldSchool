import osrs

npc_chat_head_widget = '231,4'
player_chat_widget = '217,6'
chat_holder_widget = '231,0'
quest_complete_widget = '153,4'


def start_quest():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['wizard mizgog'])
    qh.set_chat_options()
    qh.set_widgets({npc_chat_head_widget, player_chat_widget, chat_holder_widget})
    final_dialogue_seen = False
    while True:
        qh.query_backend()
        if final_dialogue_seen:
            return
        elif qh.get_chat_options('Give me a quest please.'):
            osrs.keeb.write(str(qh.get_chat_options('Give me a quest please.')))
        elif qh.get_chat_options('Yes.'):
            osrs.keeb.write(str(qh.get_chat_options('Yes.')))
            final_dialogue_seen = True
        elif qh.get_widgets(player_chat_widget) or qh.get_widgets(npc_chat_head_widget):
            osrs.keeb.press_key('space')
        elif not qh.get_widgets(chat_holder_widget) and not bool(qh.get_chat_options()):
            if len(qh.get_npcs_by_name()) > 0:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])


def finish_quest():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['wizard mizgog'])
    qh.set_chat_options()
    qh.set_widgets({npc_chat_head_widget, player_chat_widget, chat_holder_widget, quest_complete_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(quest_complete_widget):
            osrs.keeb.press_key('esc')
            return
        elif qh.get_widgets(player_chat_widget) or qh.get_widgets(npc_chat_head_widget):
            osrs.keeb.press_key('space')
        elif not qh.get_widgets(chat_holder_widget) and not bool(qh.get_chat_options()):
            if len(qh.get_npcs_by_name()) > 0:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])


def main():
    start_quest()
    finish_quest()
