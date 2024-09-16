import datetime

import osrs.bank
main_chat_widget = '162,34'
quest_complete_widget = '153,4'
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


def dialogue_handler(desired_replies=None, timeout=3):

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
            print('here')
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


def hop_to(world):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_world()
    qh.set_game_state()
    while True:
        qh.query_backend()
        if qh.get_world() == world and qh.get_game_state() == 'LOGGED_IN':
            osrs.keeb.press_key('esc')
            return
        elif qh.get_game_state() == 'LOGIN_SCREEN':
            osrs.game.login_v4()
        elif qh.get_game_state() != 'HOPPING':
            osrs.keeb.press_key('enter')
            osrs.keeb.write(f'::hop {world}')
            osrs.keeb.press_key('enter')
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()


def equip_air_staff_and_earth_strike():
    configured_spell_widget = '593,26'
    earth_strike_widget = '201,1,3'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_widgets({configured_spell_widget, earth_strike_widget})
    osrs.keeb.press_key('f1')
    osrs.keeb.press_key('esc')
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.STAFF_OF_AIR):
            osrs.move.click(qh.get_inventory(osrs.item_ids.STAFF_OF_AIR))
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            break
    last_config_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        osrs.keeb.press_key('f1')
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        if (qh.get_widgets(configured_spell_widget)
                and not qh.get_widgets(configured_spell_widget)['isHidden']
                and (datetime.datetime.now() - last_config_click).total_seconds() > 3):
            osrs.move.click(qh.get_widgets(configured_spell_widget))
            last_config_click = datetime.datetime.now()
        elif qh.get_widgets(earth_strike_widget) and not qh.get_widgets(earth_strike_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(earth_strike_widget))
            osrs.keeb.press_key('esc')
            return


def equip_staff_and_set_autocast(staff, spell_widget_id, defensive=False):
    configured_spell_widget = '593,26' if not defensive else '593,21'
    earth_strike_widget = spell_widget_id
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_equipment()
    qh.set_widgets({configured_spell_widget, earth_strike_widget})
    osrs.keeb.press_key('f1')
    osrs.keeb.press_key('esc')
    last_config_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_inventory(staff):
            osrs.keeb.press_key('esc')
            osrs.keeb.press_key('esc')
            osrs.move.click(qh.get_inventory(staff))
        elif (qh.get_widgets(configured_spell_widget)
                and not qh.get_widgets(configured_spell_widget)['isHidden']
                and (datetime.datetime.now() - last_config_click).total_seconds() > 3):
            osrs.move.click(qh.get_widgets(configured_spell_widget))
            last_config_click = datetime.datetime.now()
        elif qh.get_widgets(earth_strike_widget) and not qh.get_widgets(earth_strike_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(earth_strike_widget))
            osrs.keeb.press_key('esc')
            return
        else:
            osrs.keeb.press_key('f1')



def tab_to_varrock():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in varrock center
        if 3195 <= qh.get_player_world_location('x') <= 3226 and 3419 <= qh.get_player_world_location(
                'y') <= 3438:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT) and (datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT))
            last_tab = datetime.datetime.now()


# useful during cutscenes
def wait_for_dialogue():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
            return


def check_for_dialogue():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.query_backend()
    if qh.get_widgets(main_chat_widget) and not qh.get_widgets(main_chat_widget)['isHidden']:
        return True



def wait_for_quest_complete_screen():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({quest_complete_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(quest_complete_widget):
            osrs.keeb.press_key('esc')
            return


def kill_vampire():
    coffin_id = 46237
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['count draynor'])
    qh.set_objects_v2(
        'game',
        {coffin_id}
    )
    qh.set_interating_with()
    qh.set_widgets({quest_complete_widget})
    qh.set_active_prayers()
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    while True:
        qh.query_backend()
        if qh.get_widgets(quest_complete_widget):
            osrs.keeb.press_key('esc')
            osrs.player.turn_off_all_prayers()
            return
        elif qh.get_interating_with():
            osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
            print('fighting vamp')
        elif qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_objects_v2('game', coffin_id):
            osrs.move.fast_click(qh.get_objects_v2('game', coffin_id)[0])


def dye_goblin_mail():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        mail = qh.get_inventory(osrs.item_ids.GOBLIN_MAIL)
        blue_dye = qh.get_inventory(osrs.item_ids.BLUE_DYE)
        if mail and blue_dye:
            osrs.move.click(blue_dye)
            osrs.move.click(mail)
            break
    osrs.clock.random_sleep(1, 1.1)
    while True:
        qh.query_backend()
        mail = qh.get_inventory(osrs.item_ids.GOBLIN_MAIL)
        orange_dye = qh.get_inventory(osrs.item_ids.ORANGE_DYE)
        if mail and blue_dye:
            osrs.move.click(orange_dye)
            osrs.move.click(mail)
            break


def talk_to_npc(name, right_click=False):
    qh = osrs.queryHelper.QueryHelper()
    if type(name) is str:
        qh.set_npcs_by_name([name])
    elif type(name) is int:
        qh.set_npcs([str(name)])
    qh.set_chat_options()
    qh.set_widgets({main_chat_widget})
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_chat_options() or qh.get_widgets(main_chat_widget):
            return
        elif qh.get_npcs_by_name():
            if right_click:
                osrs.move.right_click_v6(qh.get_npcs_by_name()[0], 'Talk-to', qh.get_canvas(), in_inv=True)
            else:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_npcs():
            if right_click:
                osrs.move.right_click_v6(qh.get_npcs()[0], 'Talk-to', qh.get_canvas(), in_inv=True)
            else:
                osrs.move.fast_click(qh.get_npcs_by_name()[0])


def equip_item(item):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(item):
            osrs.move.click(qh.get_inventory(item))
            return


def enchant_meats():
    gate = 2143
    cauldron = 2142
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'prayer'})
    qh.set_active_prayers()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_objects_v2('wall', {gate})
    qh.set_objects_v2('game', {cauldron})
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    osrs.player.toggle_run('on')
    while True:
        qh.query_backend()
        osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
        osrs.combat_utils.pot_handler(qh, {})
        if qh.get_player_world_location('x') >= 2889:
            osrs.player.turn_off_all_prayers()
            break
        elif qh.get_objects_v2('wall', gate):
            osrs.move.fast_click(qh.get_objects_v2('wall', gate)[0])

    while True:
        qh.query_backend()
        item = qh.get_inventory([
            osrs.item_ids.RAW_CHICKEN,
            osrs.item_ids.RAW_BEAR_MEAT,
            osrs.item_ids.RAW_RAT_MEAT,
            osrs.item_ids.RAW_BEEF,
        ])
        if item:
            if qh.get_objects_v2('game', cauldron):
                osrs.move.click(item)
                osrs.move.click(qh.get_objects_v2('game', cauldron)[0])
                osrs.clock.random_sleep(1, 1.1)
        else:
            break


def leave_cauldron():
    gate = 2143
    ladder = 17385
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'prayer'})
    qh.set_active_prayers()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_objects_v2('wall', {gate})
    qh.set_objects_v2('game', {ladder})
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    osrs.player.toggle_run('on')
    while True:
        qh.query_backend()
        osrs.combat_utils.pot_handler(qh, {})
        if qh.get_player_world_location('x') <= 2888 and 9828 <= qh.get_player_world_location('y') <= 9832:
            osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2883, 'y': 9801, 'z': 0})
        elif qh.get_objects_v2('wall', gate) and qh.get_player_world_location('x') >= 2889:
            osrs.move.fast_click(qh.get_objects_v2('wall', gate)[0])
        elif 2881 <= qh.get_player_world_location('x') <= 2887 and 9794 <= qh.get_player_world_location('y') <= 9803 and qh.get_objects_v2('game', ladder, 7):
            osrs.move.click(qh.get_objects_v2('game', ladder, 7)[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('y') <= 5000:
            osrs.player.toggle_run('off')
            osrs.player.turn_off_all_prayers()
            return


def walk_through_door(
        door_id, coord_type, coord_value, greater_than, door_dist=15,
        intermediate_tile=None, door_type='wall', timeout=0.1
):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects_v2(door_type, {door_id})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    if intermediate_tile:
        qh.set_tiles({intermediate_tile})
    while True:
        qh.query_backend()
        if greater_than and qh.get_player_world_location(coord_type) >= coord_value:
            return
        elif not greater_than and qh.get_player_world_location(coord_type) <= coord_value:
            return
        elif (qh.get_objects_v2(door_type, door_id, door_dist)
              and (datetime.datetime.now() - last_click).total_seconds() > timeout):
            osrs.move.fast_click(qh.get_objects_v2(door_type, door_id, door_dist)[0])
            last_click = datetime.datetime.now()
        elif intermediate_tile and qh.get_tiles(intermediate_tile) and not qh.get_objects_v2(door_type, door_id, door_dist):
            osrs.move.fast_click(qh.get_tiles(intermediate_tile))


def interact_with_object(
        door_id, coord_type, coord_value, greater_than, door_dist=15,
        intermediate_tile=None, door_type='wall', timeout=0.1, custom_exit_function=None, custom_exit_function_arg=None,
        pre_interact=None, obj_tile=None
):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects_v2(door_type, {door_id})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    if intermediate_tile:
        qh.set_tiles({intermediate_tile})
    while True:
        qh.query_backend()
        target_obj = qh.get_objects_v2(door_type, door_id, door_dist)
        if target_obj and obj_tile:
            target_obj = list(
                filter(lambda obj: obj['x_coord'] == obj_tile['x'] and obj['y_coord'] == obj_tile['y'], target_obj)
            )
        if not custom_exit_function:
            if greater_than and qh.get_player_world_location(coord_type) >= coord_value:
                return
            elif not greater_than and qh.get_player_world_location(coord_type) <= coord_value:
                return
        else:
            if custom_exit_function_arg is not None and custom_exit_function(custom_exit_function_arg):
                return True
            elif custom_exit_function_arg is None and custom_exit_function():
                return True

        if target_obj and (datetime.datetime.now() - last_click).total_seconds() > timeout:
            if pre_interact:
                pre_interact()
            osrs.move.fast_click(target_obj[0])
            last_click = datetime.datetime.now()
        elif intermediate_tile and qh.get_tiles(intermediate_tile) and not target_obj:
            osrs.move.fast_click(qh.get_tiles(intermediate_tile))


def recharge_prayer_at_alter():
    altar = 14860
    altar1 = 409
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {altar, altar1})
    qh.set_skills({'prayer'})
    while True:
        qh.query_backend()
        if qh.get_skills('prayer') and qh.get_skills('prayer')['level'] == qh.get_skills('prayer')['boostedLevel']:
            return
        elif qh.get_objects_v2('game'):
            osrs.move.fast_click(qh.get_objects_v2('game')[0])


def help_femi():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({main_chat_widget})
    qh.set_objects_v2('game', {190})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 3384:
            return
        if qh.get_widgets(main_chat_widget):
            dialogue_handler(["Okay then."])
        elif qh.get_objects_v2('game', 190):
            osrs.move.fast_click(qh.get_objects_v2('game', 190)[0])


def kill_single_npc(npc, prayers, pots):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([npc])
    qh.set_interating_with()
    fought = False
    while True:
        qh.query_backend()
        osrs.combat_utils.prayer_handler(None, prayers)
        osrs.combat_utils.pot_handler(None, pots)
        if qh.get_npcs_by_name() and not qh.get_interating_with():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])
        elif qh.get_interating_with():
            fought = True
            print('in combat')
        elif not qh.get_npcs_by_name() and fought:
            return
        osrs.keeb.press_key('space')


def check_for_item_in_inv(item):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(item):
        return True


def turn_off_doors_in_house():
    options_widget = '161,47'
    house_widget = '116,31'
    no_doors_widget = '370,19'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({options_widget, house_widget, no_doors_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(no_doors_widget) and not qh.get_widgets(no_doors_widget)['isHidden']:
            if qh.get_widgets(no_doors_widget)['spriteID'] == 699:
                osrs.clock.sleep_one_tick()
                osrs.keeb.press_key('esc')
                osrs.keeb.press_key('esc')
                return
            osrs.move.click(qh.get_widgets(no_doors_widget))
        elif qh.get_widgets(house_widget) and not qh.get_widgets(house_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(house_widget))
        elif qh.get_widgets(options_widget) and not qh.get_widgets(options_widget)['isHidden']:
            osrs.move.click(qh.get_widgets(options_widget))


def drop_hammer_and_saw():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    while True:
        qh.query_backend()
        if qh.get_inventory([osrs.item_ids.SAW, osrs.item_ids.HAMMER]):
            osrs.move.right_click_v6(
                qh.get_inventory([osrs.item_ids.SAW, osrs.item_ids.HAMMER]),
                'Drop',
                qh.get_canvas(),
                in_inv=True
            )
        else:
            return