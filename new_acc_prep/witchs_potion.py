import datetime

import osrs
import util_functions
import transport_functions


dialogue = [
    "I am in search of a quest.", "Yes.",
    "Yes, help me become one with my darker side."
]


def kill_rat_and_get_tail():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['rat'])
    qh.set_inventory()
    qh.set_interating_with()
    qh.query_backend()
    while True:
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(10, qh.get_player_world_location())
        qh.set_ground_items(nearby_tiles)
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.RATS_TAIL.value):
            return
        elif qh.get_ground_items():
            tail = list(filter(lambda item: item['id'] == osrs.item_ids.ItemIDs.RATS_TAIL.value, qh.get_ground_items()))
            if len(tail) > 0:
                osrs.move.fast_click(tail[0])

        if not qh.get_interating_with() and len(qh.get_npcs_by_name()) > 0:
            osrs.move.fast_click(qh.get_npcs_by_name()[0])


def give_ingredients():
    chat_holder_widget = '217,1'
    chat_holder2_widget = '231,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs_by_name(['hetty'])
    qh.set_chat_options()
    qh.set_widgets({chat_holder_widget, chat_holder2_widget})
    while True:
        qh.query_backend()
        if (not qh.get_chat_options()
                and not qh.get_widgets(chat_holder_widget)
                and not qh.get_widgets(chat_holder2_widget) and len(qh.get_npcs_by_name()) > 0):
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        else:
            success = util_functions.dialogue_handler()
            if success:
                return


def drink_from_cauldron():
    quest_complete_widget = '153,4'
    cauldron_id = '2024'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects(
        {'2967,3205,0'},
        {cauldron_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_widgets({quest_complete_widget})
    last_c_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(quest_complete_widget):
            osrs.keeb.press_key('esc')
            return
        elif (qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cauldron_id)
              and (datetime.datetime.now() - last_c_click).total_seconds() > 4):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, cauldron_id)[0])
            last_c_click = datetime.datetime.now()
        util_functions.dialogue_handler()


def main():
    osrs.move.interact_with_object(
        1535, 'x', 2965, True, obj_type='wall',
        obj_tile={'x': 2964, 'y': 3206}, intermediate_tile='2967,3205,0'
    )
    util_functions.talk_to_npc('hetty')
    util_functions.dialogue_handler(dialogue)
    osrs.move.interact_with_object(
        1535, 'x', 2964, False, obj_type='wall',
        obj_tile={'x': 2964, 'y': 3206}, intermediate_tile='2962,3205,0'
    )
    kill_rat_and_get_tail()
    osrs.move.go_to_loc(2959, 3209)
    osrs.move.interact_with_object(
        1535, 'x', 2965, True, obj_type='wall',
        obj_tile={'x': 2964, 'y': 3206}, intermediate_tile='2967,3205,0'
    )
    util_functions.talk_to_npc('hetty')
    util_functions.dialogue_handler(dialogue)
    drink_from_cauldron()
    osrs.move.interact_with_object(
        1535, 'x', 2964, False, obj_type='wall',
        obj_tile={'x': 2964, 'y': 3206}, intermediate_tile='2962,3205,0'
    )