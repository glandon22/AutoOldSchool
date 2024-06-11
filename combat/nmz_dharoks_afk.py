import datetime

import osrs

absorption_varbit= '3956'

def create_dream():
    npc_text_dialogue_widget = '231,6'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['dominic onion'])
    qh.set_chat_options()
    qh.set_widgets({npc_text_dialogue_widget})
    while True:
        qh.query_backend()
        if not qh.get_chat_options() and qh.get_npcs_by_name() and not qh.get_widgets(npc_text_dialogue_widget):
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)
        elif qh.get_chat_options('Previous: Customisable Rumble (hard)'):
            osrs.keeb.write(str(qh.get_chat_options('Previous: Customisable Rumble (hard)')))
        elif qh.get_chat_options('rumble'):
            osrs.keeb.write(str(qh.get_chat_options('rumble')))
        elif qh.get_chat_options('customisable - hard'):
            osrs.keeb.write(str(qh.get_chat_options('customisable - hard')))
        elif qh.get_widgets(npc_text_dialogue_widget) and 'customisable Rumble dream, hard mode' in qh.get_widgets(npc_text_dialogue_widget)['text']:
            osrs.keeb.press_key('space')
        elif qh.get_chat_options('yes'):
            return osrs.keeb.write(str(qh.get_chat_options('yes')))


def enter_dream():
    accept_dream_widget_id = '129,6'
    dream_vial_id = '26291'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {"2605,3117,0"},
        {dream_vial_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_widgets({accept_dream_widget_id})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') > 9000 or qh.get_player_world_location('x') > 5700:
            osrs.clock.random_sleep(2, 2.1)
            osrs.keeb.press_key('esc')
            return print(qh.get_player_world_location())
        elif qh.get_widgets(accept_dream_widget_id):
            osrs.move.fast_click(qh.get_widgets(accept_dream_widget_id))
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dream_vial_id) \
                and (datetime.datetime.now() - last_click).total_seconds() > 5:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, dream_vial_id)[0])
            last_click = datetime.datetime.now()


def kill_monsters():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_varbit(absorption_varbit)
    qh.set_skills({'hitpoints', 'strength'})
    qh.set_npcs_by_name([])
    qh.set_inventory()
    last_rapid_heal_flick = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] != 1:
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.DWARVEN_ROCK_CAKE.value))



enter_dream()