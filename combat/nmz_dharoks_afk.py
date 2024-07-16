import datetime

import osrs


'''
customisable hard rumble
trapped soul
count draynor corsair traitor
sand snake
king roald
kendal
me 
skele hellhound
tree spirit 
khazard warlord 
b knight titan
bouncer 
blk demon
jung demon

'''

over_loads = [
    11730,
    11731,
    11732,
    11733,
]

absorption = [
    11734,
    11735,
    11736,
    11737,
]
absorption_varbit = '3956'


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
        elif qh.get_widgets(npc_text_dialogue_widget) and 'customisable Rumble dream, hard mode' in \
                qh.get_widgets(npc_text_dialogue_widget)['text']:
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
    recurrent_id = '26265'
    zapper_id = '26256'
    power_surge_id = '26264'
    exit_pot_id = '26276'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_varbit(absorption_varbit)
    qh.set_skills({'hitpoints', 'strength'})
    qh.set_npcs_by_name([])
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_player_world_location()
    last_rapid_heal_flick = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_overload_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    session_start_time = datetime.datetime.now()
    while True:
        qh.query_backend()
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(15, qh.get_player_world_location())
        qh.clear_objects(osrs.queryHelper.ObjectTypes.GAME.value)
        qh.set_objects(
            set(nearby_tiles),
            {zapper_id, exit_pot_id, power_surge_id, recurrent_id},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        if qh.get_player_world_location('x') < 5700:
            return

        if (datetime.datetime.now() - session_start_time).total_seconds() > 3420:
            continue

        # dont rock cake down until my health is fully reduced from the overload otherwise i will die!
        if qh.get_varbit() < 50 and osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), absorption):
            osrs.move.fast_click(osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), absorption))
            osrs.clock.random_sleep(0.2, 0.3)
        elif qh.get_skills('strength') \
                and qh.get_skills('strength')['boostedLevel'] <= qh.get_skills('strength')['level'] \
                and osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), over_loads):
            osrs.move.click(osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), over_loads))
            last_overload_click = datetime.datetime.now()
        elif qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] != 1 \
                and (datetime.datetime.now() - last_overload_click).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.DWARVEN_ROCK_CAKE_7510.value))
        elif (datetime.datetime.now() - last_rapid_heal_flick).total_seconds() > 30:
            osrs.player.flick_all_prayers()
            last_rapid_heal_flick = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, zapper_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, zapper_id)[0])
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, recurrent_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, recurrent_id)[0])
        elif not qh.get_interating_with() and qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)


# Work in progress
def get_absorps_and_overloads():
    chat_input_request_widget = '162,41'
    absorp_barrel_id = '26280'
    overload_barrel_id = '26279'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({chat_input_request_widget})
    qh.set_objects(
        {'2600,3117,0', '2600,3116,0'},
        {absorp_barrel_id, overload_barrel_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_chat_options()
    qh.set_inventory()
    last_abs_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_over_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, absorp_barrel_id) and (datetime.datetime.now() - last_abs_click).total_seconds() > 7:
            osrs.move.right_click_v5(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, absorp_barrel_id)[0], 'Store')
            last_abs_click = datetime.datetime.now()
        elif qh.get_chat_options('yes, please.'):
            osrs.keeb.write(str(qh.get_chat_options('yes, please.')))
        elif not osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), absorption):
            last_abs_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            break
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, overload_barrel_id) and (datetime.datetime.now() - last_over_click).total_seconds() > 7:
            osrs.move.right_click_v5(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, overload_barrel_id)[0], 'Store')
            last_over_click = datetime.datetime.now()
        elif qh.get_chat_options('yes, please.'):
            osrs.keeb.write(str(qh.get_chat_options('yes, please.')))
        elif not osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), over_loads):
            last_over_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            break
    for item in qh.get_inventory():
        if item['id'] != osrs.item_ids.ItemIDs.DWARVEN_ROCK_CAKE_7510.value:
            osrs.move.right_click_v5(item, 'Drop', in_inv=True)
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, overload_barrel_id) and (datetime.datetime.now() - last_over_click).total_seconds() > 7:
            osrs.move.right_click_v5(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, overload_barrel_id)[0], 'Take')
            last_over_click = datetime.datetime.now()
        elif osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), over_loads):
            break
        elif qh.get_widgets(chat_input_request_widget):
            print(qh.get_widgets(chat_input_request_widget))
            osrs.clock.random_sleep(1, 1.1)
            osrs.keeb.write('16')
            osrs.keeb.press_key('enter')
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, absorp_barrel_id) and (datetime.datetime.now() - last_abs_click).total_seconds() > 7:
            osrs.move.right_click_v5(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, absorp_barrel_id)[0], 'Take')
            last_abs_click = datetime.datetime.now()
        elif osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), absorption):
            break
        elif qh.get_widgets(chat_input_request_widget):
            print(qh.get_widgets(chat_input_request_widget))
            osrs.clock.random_sleep(1, 1.1)
            osrs.keeb.write('80')
            osrs.keeb.press_key('enter')


def main():
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'low',
            'login': False,
            'logout': False
        })
        create_dream()
        get_absorps_and_overloads()
        enter_dream()
        kill_monsters()
