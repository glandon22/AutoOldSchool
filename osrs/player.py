import datetime

import osrs.move as move
import osrs.queryHelper
import osrs.server as server
import osrs.dev as dev
from osrs.widget_ids import WidgetIDs
import logging

def toggle_prayer_slow(desired_state, port):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1066, 'off': 1063}[desired_state]
    while True:
        prayer_orb = server.get_widget('160,21', port)
        if prayer_orb:
            if prayer_orb['spriteID'] != desired_state:
                move.move_and_click(prayer_orb['x'], prayer_orb['y'], 3, 3)
            return


def toggle_prayer(desired_state, port='56799'):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1066, 'off': 1063}[desired_state]
    while True:
        prayer_orb = server.get_widget('160,21', port)
        if prayer_orb:
            if prayer_orb['spriteID'] != desired_state:
                move.fast_move_and_click(prayer_orb['x'], prayer_orb['y'], 3, 3)
            return


def turn_off_all_prayers():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_active_prayers()
    qh.set_widgets({'160,21'})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if not qh.get_active_prayers():
            return
        elif qh.get_widgets('160,21') and (datetime.datetime.now() - last_click).total_seconds() > 1:
            osrs.move.click(qh.get_widgets('160,21'))
            osrs.move.click(qh.get_widgets('160,21'))
            last_click = datetime.datetime.now()

def flick_all_prayers():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_active_prayers()
    qh.set_widgets({'160,21'})
    while True:
        qh.query_backend()
        if qh.get_widgets('160,21'):
            osrs.move.fast_click(qh.get_widgets('160,21'))
            osrs.clock.random_sleep(0.2, 0.3)
            osrs.move.fast_click(qh.get_widgets('160,21'))
            return


def toggle_run(desired_state, port='56799'):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1065, 'off': 1064}[desired_state]
    while True:
        run_orb = server.get_widget('160,29', port)
        if run_orb:
            if run_orb['spriteID'] != desired_state:
                move.fast_move_and_click(run_orb['x'], run_orb['y'], 3, 3)
            return


def get_run_energy():
    while True:
        logging.info('getting run energy.')
        run_orb = server.get_widget('160,28')
        if run_orb:
            logging.info('got run energy: {}'.format(run_orb))
            return int(run_orb['text'])


def toggle_auto_retaliate(state):
    auto_retaliate_widget = '593,33'
    desired_outcome = {
        'on': 1749,
        'off': 1748
    }[state]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({auto_retaliate_widget})
    last_key_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_widget_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if (not qh.get_widgets(auto_retaliate_widget) or qh.get_widgets(auto_retaliate_widget)['isHidden']) and \
                (datetime.datetime.now() - last_key_press).total_seconds() > 0.8:
            osrs.keeb.press_key('f1')
            last_key_press = datetime.datetime.now()
        elif qh.get_widgets(auto_retaliate_widget) and qh.get_widgets(auto_retaliate_widget)['spriteID'] == desired_outcome:
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('esc')
            return
        elif qh.get_widgets(auto_retaliate_widget) and (datetime.datetime.now() - last_widget_click).total_seconds() > 1.3:
            osrs.move.click(qh.get_widgets(auto_retaliate_widget))
            last_widget_click = datetime.datetime.now()


def dialogue_handler(desired_replies=None, timeout=3):
    main_chat_widget = '162,34'
    npc_chat_head_widget = '231,4'
    player_chat_widget = '217,6'
    chat_holder_widget = '231,0'
    chat_holder2_widget = '217,1'
    click_to_continue_widget = '229,2'
    click_to_continue_level_widget = '233,2'
    click_to_continue_other_widget = '193,0,2'
    #
    # quest_complete_widget = '153,4'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_chat_options()
    qh.set_widgets({
        npc_chat_head_widget, player_chat_widget,
        chat_holder_widget, chat_holder2_widget,
        click_to_continue_widget, main_chat_widget, click_to_continue_level_widget,
        click_to_continue_other_widget
    })
    had_dialogue = False
    dialogue_last_seen = datetime.datetime.now()
    while True:
        qh.query_backend()
        if (
                not qh.get_widgets(main_chat_widget)
                or (qh.get_widgets(main_chat_widget) and qh.get_widgets(main_chat_widget)['isHidden'])
        ):
            if (datetime.datetime.now() - dialogue_last_seen).total_seconds() > timeout:
                return had_dialogue
        else:
            print('dialogue box is open.')
            dialogue_last_seen = datetime.datetime.now()

        if desired_replies:
            for reply in desired_replies:
                if qh.get_chat_options(reply):
                    osrs.keeb.write(str(qh.get_chat_options(reply)))
                    had_dialogue = True
        if (qh.get_widgets(player_chat_widget)
                or qh.get_widgets(npc_chat_head_widget)
                or qh.get_widgets(click_to_continue_level_widget)
                or qh.get_widgets(click_to_continue_other_widget)
                or qh.get_widgets(click_to_continue_widget)):
            osrs.keeb.press_key('space')
            had_dialogue = True


def equip_item(items):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_equipment()
    qh.set_inventory()
    clicked = {

    }
    while True:
        qh.query_backend()
        if qh.get_equipment() and set(items).issubset(qh.get_equipment()):
            return
        elif qh.get_inventory():
            for item in qh.get_inventory():
                if item['id'] in items and (item['id'] not in clicked or (datetime.datetime.now() - clicked[item['id']]).total_seconds() > 1):
                    osrs.move.fast_click(item)
                    clicked[item['id']] = datetime.datetime.now()
