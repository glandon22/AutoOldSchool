import datetime

import cooks_assistant
import osrs.bank
import transport_functions


def get_quest_items(items):
    banking_config = {
        'dump_inv': True,
        'dump_equipment': True,
        'withdraw': [{'items': items}]
    }
    success = osrs.bank.banking_handler(
        banking_config
    )

    if not success:
        return print('failed to bank in lum')


def dialogue_handler(desired_replies=None):
    npc_chat_head_widget = '231,4'
    player_chat_widget = '217,6'
    chat_holder_widget = '231,0'
    chat_holder2_widget = '217,1'
    click_to_continue_widget = '229,2'
    #
    # quest_complete_widget = '153,4'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_widgets({npc_chat_head_widget, player_chat_widget, chat_holder_widget, chat_holder2_widget, click_to_continue_widget})
    had_dialogue = False
    dialogue_last_seen = datetime.datetime.now()
    while True:
        qh.query_backend()
        if (
                (not qh.get_widgets(chat_holder_widget) or not qh.get_widgets(chat_holder2_widget))
                and not qh.get_chat_options()
        ):
            if (datetime.datetime.now() - dialogue_last_seen).total_seconds() > 3:
                return had_dialogue
        else:
            print('here')
            dialogue_last_seen = datetime.datetime.now()

        if desired_replies:
            for reply in desired_replies:
                if qh.get_chat_options(reply):
                    osrs.keeb.write(str(qh.get_chat_options(reply)))
                    had_dialogue = True
        if (qh.get_widgets(player_chat_widget)
                or qh.get_widgets(npc_chat_head_widget)
                or qh.get_widgets(click_to_continue_widget)):
            osrs.keeb.press_key('space')
            had_dialogue = True


def hop_to_330():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_world()
    qh.set_game_state()
    while True:
        qh.query_backend()
        if qh.get_world() == 330:
            osrs.keeb.press_key('esc')
            return
        elif qh.get_game_state() != 'HOPPING':
            osrs.keeb.press_key('enter')
            osrs.keeb.write('::hop 330')
            osrs.keeb.press_key('enter')
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
