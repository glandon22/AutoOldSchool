import datetime

# active body portal 43709
# body altar 34765
# body exit portal 34753

# nature portal 43711
# altar 34768
# exit 34756

# mind portal 43705
# altar 34761
# exit 34749

# portal you can pass thru to start game 43700

from osrs_utils import general_utils

port = '56799'
frag_portal_dict = {
    'S': {'x': 3615, 'y': 9490, 'z': 0},
    'E': {'x': 3628, 'y': 9499, 'z': 0},
    'SE': {'x': 3623, 'y': 9495, 'z': 0},
    'SW': {'x': 3607, 'y': 9492, 'z': 0}
}


sprite_to_rift_obj_dict = {
    '4353': { # air
        'tile': '3617,9494,0',
        'id': '43701',
        'tile_obj': {
            'x': 3617,
            'y': 9494,
            'z': 0
        }
    },
    '4359' : { # cosmic
        'tile': '3621,9496,0',
        'id': '43710',
        'tile_obj': {
            'x': 3621,
            'y': 9496,
            'z': 0
        }
    },
    '4355' : { # water
        'tile': '3623,9500,0',
        'id': '43702',
        'tile_obj': {
            'x': 3623,
            'y': 9500,
            'z': 0
        }
    },
    '4356' : { # earth
        'tile': '3623,9505,0',
        'id': '43703',
        'tile_obj': {
            'x': 3623,
            'y': 9505,
            'z': 0
        }
    },
    '4361' : { # nat
        'tile': '3621,9509,0',
        'id': '43711',
        'tile_obj': {
            'x': 3621,
            'y': 9509,
            'z': 0
        }
    },
    '4357' : { # fire
        'tile': '3617,9511,0',
        'id': '43704',
        'tile_obj': {
            'x': 3617,
            'y': 9511,
            'z': 0
        }
    },
    '4364' : { # blood
        'tile': '3612,9511,0',
        'id': '43708',
        'tile_obj': {
            'x': 3612,
            'y': 9511,
            'z': 0
        }
    },
    '4362' : { # law
        'tile': '3609,9510,0',
        'id': '43712',
        'tile_obj': {
            'x': 3609,
            'y': 9510,
            'z': 0
        }
    },
    '4363' : { # death
        'tile': '3607,9506,0',
        'id': '43707',
        'tile_obj': {
            'x': 3607,
            'y': 9506,
            'z': 0
        }
    },
    '4360' : { # chaos
        'tile': '3607,9501,0',
        'id': '43706',
        'tile_obj': {
            'x': 3607,
            'y': 9501,
            'z': 0
        }
    },
    '4358' : { # body
        'tile': '3609,9497,0',
        'id': '43709',
        'tile_obj': {
            'x': 3609,
            'y': 9497,
            'z': 0
        }
    },
    '4354' : { # mind
        'tile': '3612,9495,0',
        'id': '43705',
        'tile_obj': {
            'x': 3612,
            'y': 9495,
            'z': 0
        }
    }
}


def game_active():
    elem = general_utils.get_widget('746,23')
    return bool(elem)


def is_pregame():
    beginning = general_utils.get_widget('746,23')
    if beginning and 'spriteID' in beginning and beginning['spriteID'] == 4369:
        return True
    return False


def in_main_arena():
    print('calling in main arena')
    loc = general_utils.get_world_location(port)
    if loc and 'x' in loc and 3597 <= loc['x'] <= 3633 and 'y' in loc and 9484 <= loc['y'] <= 9519:
        return True
    else:
        return False


def take_uncharged_cells(status_obj):
    inv = general_utils.get_inv(port)
    uncharged_cell = general_utils.is_item_in_inventory_v2(inv, 26882)
    if in_main_arena() and not game_active() and not uncharged_cell:
        table = general_utils.get_game_object('3618,9488,0', '43732', port)
        if table:
            general_utils.right_click_menu_select(table, None, port, 'Uncharged cells', 'Take-10')
            return {**status_obj, '43732': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 3618, 'y': 9488, 'z': 0}, port)
    return status_obj


def run_to_large_remains(status_obj):
    print('calling run to large remains')
    inv = general_utils.get_inv(port)
    uncharged_cell = general_utils.is_item_in_inventory_v2(inv, 26882)
    if (not game_active() or is_pregame()) and general_utils.get_target_obj(port) != 43724 and in_main_arena() and uncharged_cell:
        obstacle = general_utils.get_ground_object('3634,9503,0', '43724', port)
        if bool(obstacle):
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            return {**status_obj, '43724': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 3626, 'y': 9500, 'z': 0}, port)
    return status_obj


def mine_large_remains(status_obj):
    print('calling mine large remains')
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    if 'x' in loc and loc['x'] >= 3637 and \
            (not guardian_frags or guardian_frags and guardian_frags['quantity'] < 180) \
            and not general_utils.is_mining(port) and game_active(): # and general_utils.get_target_obj(port) != 43719
        rock = general_utils.get_game_object('3640,9498,0', '43719', port)
        if rock:
            general_utils.move_and_click(rock['x'], rock['y'], 3, 3)
            return {**status_obj, '43719': datetime.datetime.now()}
    return status_obj


def leave_large_remains_area(status_obj):
    print('calling leave large remains')
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    beginning = general_utils.get_widget('746,23')
    if 'x' in loc and loc['x'] >= 3637 and \
            guardian_frags and guardian_frags['quantity'] > 180 \
            and beginning and 'spriteID' in beginning and beginning['spriteID'] != 4369 and general_utils.get_target_obj(port) != 43726:
        obstacle = general_utils.get_ground_object('3636,9503,0', '43726', port)
        if obstacle:
            general_utils.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            general_utils.sleep_one_tick()
            return {**status_obj, '43726': datetime.datetime.now()}
    return status_obj


def frag_port_available(status_obj):
    print('calling frag port available')
    portal_text = general_utils.get_widget('746,28', port)
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    if portal_text and loc and 'x' in loc and 3597 <= loc['x'] <= 3633 and len(inv) < 28 and general_utils.get_target_obj(port) != 43729:
        text_parts = portal_text['text'].split(' - ')
        if len(text_parts) >= 2 and text_parts[1] != '0:00':
            print('b', text_parts[0])
            general_utils.run_towards_square_v2(frag_portal_dict[text_parts[0]], port)
            orb = general_utils.get_surrounding_game_objects(10, ['43729'], port)
            if orb and '43729' in orb:
                general_utils.move_and_click(orb['43729']['x'], orb['43729']['y'], 1, 1)
                general_utils.sleep_one_tick()
                general_utils.wait_until_stationary(port)
                return {**status_obj, '43729': datetime.datetime.now()}
    return status_obj


def mine_huge_remains(status_obj):
    print('calling mine huge remains')
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    if loc and 'x' in loc and loc['x'] <= 3594 and len(inv) < 28 and not general_utils.is_mining(port) and general_utils.get_target_obj(port) != 43720 and game_active():
        remains = general_utils.get_surrounding_game_objects(8, ['43720'], port)
        if remains and '43720' in remains:
            general_utils.move_and_click(remains['43720']['x'], remains['43720']['y'], 3, 3)
            return {**status_obj, '43720': datetime.datetime.now()}
    return status_obj


def leave_huge_remains(status_obj):
    print('calling leave huge remains')
    loc = general_utils.get_world_location(port)
    inv = general_utils.get_inv(port)
    if loc and 'x' in loc and loc['x'] <= 3594 and (len(inv) == 28 or not game_active()) and general_utils.get_target_obj(port) != 38044:
        remains = general_utils.get_game_object('3593,9503,0', '38044', port)
        if remains:
            general_utils.move_and_click(remains['x'], remains['y'], 3, 3)
            return {**status_obj, '38044': datetime.datetime.now()}
    return status_obj

'''# may want to consider refactoring this one to use the click timeouts
def make_essence():
    print('calling make ess')
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = general_utils.is_item_in_inventory_v2(inv, 26881)
    if in_main_arena() and guardian_frags and not guardian_ess and not elem_guardian_stone:
        work_table = general_utils.get_surrounding_game_objects(10, ['43754'], port)
        if not bool(work_table):
            general_utils.run_towards_square_v2({'x': 3615, 'y': 9492, 'z': 0}, port)
        work_table = general_utils.get_surrounding_game_objects(10, ['43754'], port)
        if work_table and '43754' in work_table:
            general_utils.move_and_click(work_table['43754']['x'], work_table['43754']['y'], 3, 3)
            if int(general_utils.get_target_obj(port)) == 43754:
                start_time = datetime.datetime.now()
                while True:
                    curr_inv = general_utils.get_inv(port)
                    guardian_frags = general_utils.is_item_in_inventory_v2(curr_inv, 26878)
                    if len(curr_inv) == 28 or \
                            (datetime.datetime.now() - start_time).total_seconds() > 20 or \
                            not guardian_frags:
                        break'''


def make_essencev2(status_obj):
    inv = general_utils.get_inv(port)
    guardian_frags = general_utils.is_item_in_inventory_v2(inv, 26878)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = general_utils.is_item_in_inventory_v2(inv, 26881)
    if in_main_arena() and guardian_frags and not guardian_ess and not elem_guardian_stone and general_utils.get_player_animation(port) != 9365:
        if general_utils.are_items_in_inventory_v2(inv, [554, 555, 556, 557]): #  and general_utils.get_target_obj(port) != 43696
            print('have runes')
            rune_deposit = general_utils.get_game_object('3609,9487,0', '43696', port)
            if rune_deposit:
                print('found depo')
                general_utils.move_and_click(rune_deposit['x'], rune_deposit['y'], 3, 3)
                return {**status_obj, '43696': datetime.datetime.now()}
            else:
                general_utils.run_towards_square_v2({'x': 3609, 'y': 9487, 'z': 0}, port)
        else:
            workbench = general_utils.get_game_object('3612,9487,0', '43754', port)
            if workbench:
                general_utils.move_and_click(workbench['x'], workbench['y'], 3, 3)
                return {**status_obj, '43754': datetime.datetime.now()}
            else:
                general_utils.run_towards_square_v2({'x': 3612, 'y': 9487, 'z': 0}, port)
    return status_obj


def enter_active_rift(status_obj):
    print('calling enter active rift')
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = general_utils.is_item_in_inventory_v2(inv, 26881)
    if in_main_arena() and guardian_ess and general_utils.get_player_animation(port) != 9365 and not elem_guardian_stone:
        # will do catalytic rifts later bc i cant enter most of them
        '''active_catalytic_rift = general_utils.get_widget('746,23')
        if active_catalytic_rift and 'spriteID' in active_catalytic_rift:
            rift_to_enter = sprite_to_rift_obj_dict[str(active_catalytic_rift['spriteID'])]'''
        active_elem_rift = general_utils.get_widget('746,20')
        if active_elem_rift and 'spriteID' in active_elem_rift and \
                str(active_elem_rift['spriteID']) in sprite_to_rift_obj_dict and \
                str(general_utils.get_target_obj(port)) != sprite_to_rift_obj_dict[str(active_elem_rift['spriteID'])]['id']:
            rift_to_enter = sprite_to_rift_obj_dict[str(active_elem_rift['spriteID'])]
            rift = general_utils.get_game_object(rift_to_enter['tile'], rift_to_enter['id'])
            print('rr', sprite_to_rift_obj_dict[str(active_elem_rift['spriteID'])]['id'])
            print('11', sprite_to_rift_obj_dict[str(active_elem_rift['spriteID'])])
            print('22', str(active_elem_rift['spriteID']))
            if rift:
                general_utils.move_and_click(rift['x'], rift['y'], 3, 4)
                return {**status_obj, rift_to_enter['id']: datetime.datetime.now()}
            else:
                general_utils.run_towards_square_v2(rift_to_enter['tile_obj'], port)
    return status_obj


def in_air_altar():
    loc = general_utils.get_world_location(port)
    if 'x' in loc and 2835 <= loc['x'] <= 2851:
        return True
    else:
        return False


def in_fire_altar():
    loc = general_utils.get_world_location(port)
    if 'x' in loc and 2560 <= loc['x'] <= 2605:
        return True
    else:
        return False


def in_earth_altar():
    loc = general_utils.get_world_location(port)
    if 'x' in loc and 2628 <= loc['x'] <= 2680:
        return True
    else:
        return False


def in_water_altar():
    loc = general_utils.get_world_location(port)
    if 'x' in loc and 2707 <= loc['x'] <= 2732:
        return True
    else:
        return False


def make_waters(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_water_altar() and guardian_ess and general_utils.get_target_obj(port) != 34762:
        altar = general_utils.get_game_object('2716,4836,0', '34762', port)
        if altar:
            general_utils.move_and_click(altar['x'], altar['y'], 3, 3)
            return {**status_obj, '34762': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2716, 'y': 4836, 'z': 0}, port)
    return status_obj


def make_earths(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_earth_altar() and guardian_ess and general_utils.get_target_obj(port) != 34763:
        altar = general_utils.get_game_object('2658,4841,0', '34763', port)
        if altar:
            general_utils.move_and_click(altar['x'], altar['y'], 3, 3)
            return {**status_obj, '34763': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2658, 'y': 4841, 'z': 0}, port)
    return status_obj


def make_airs(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_air_altar() and guardian_ess and general_utils.get_target_obj(port) != 34760:
        altar = general_utils.get_game_object('2844,4834,0', '34760', port)
        if altar:
            general_utils.move_and_click(altar['x'], altar['y'], 3, 3)
            return {**status_obj, '34760': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2844, 'y': 4834, 'z': 0}, port)
    return status_obj


def make_fires(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_fire_altar() and guardian_ess and general_utils.get_target_obj(port) != 34764:
        altar = general_utils.get_game_object('2585,4838,0', '34764', port)
        if altar:
            general_utils.move_and_click(altar['x'], altar['y'], 3, 3)
            return {**status_obj, '34764': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2585, 'y': 4838, 'z': 0}, port)
    return status_obj


def leave_fire_altar(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_fire_altar() and not guardian_ess and general_utils.get_target_obj(port) != 34752:
        exit = general_utils.get_game_object('2574,4850,0', '34752', port)
        if exit:
            general_utils.move_and_click(exit['x'], exit['y'], 3, 3)
            return {**status_obj, '34752': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2574, 'y': 4850, 'z': 0}, port)
    return status_obj


def leave_water_altar(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_water_altar() and not guardian_ess and general_utils.get_target_obj(port) != 34750:
        exit = general_utils.get_game_object('2727,4832,0', '34750', port)
        if exit:
            general_utils.move_and_click(exit['x'], exit['y'], 3, 3)
            return {**status_obj, '34750': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2727, 'y': 4832, 'z': 0}, port)
    return status_obj


def leave_air_altar(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_air_altar() and not guardian_ess and general_utils.get_target_obj(port) != 34748:
        exit = general_utils.get_game_object('2841,4828,0', '34748', port)
        if exit:
            general_utils.move_and_click(exit['x'], exit['y'], 3, 3)
            return {**status_obj, '34748': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2841, 'y': 4828, 'z': 0}, port)
    return status_obj


def leave_earth_altar(status_obj):
    inv = general_utils.get_inv(port)
    guardian_ess = general_utils.is_item_in_inventory_v2(inv, 26879)
    if in_earth_altar() and not guardian_ess  and general_utils.get_target_obj(port) != 34751:
        exit = general_utils.get_game_object('2655,4829,0', '34751', port)
        if exit:
            general_utils.move_and_click(exit['x'], exit['y'], 3, 3)
            return {**status_obj, '34751': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 2655, 'y': 4829, 'z': 0}, port)
    return status_obj


def charge_guardian(status_obj):
    inv = general_utils.get_inv(port)
    elem_guardian_stone = general_utils.is_item_in_inventory_v2(inv, 26881)
    if in_main_arena() and elem_guardian_stone and general_utils.get_target_npc(port) != 11403:
        guardian = general_utils.get_npcs_by_id('11403', port)
        if len(guardian) > 0:
            general_utils.move_and_click(guardian[0]['x'], guardian[0]['y'], 3, 3)
            return {**status_obj, '11403': datetime.datetime.now()}
        else:
            general_utils.run_towards_square_v2({'x': 3615, 'y': 9503, 'z': 0}, port)
    return status_obj


def main():
    general_utils.random_sleep(1, 2)
    obj_clicks = {

    }
    npc_clicks = {

    }
    while True:
        obj_clicks = run_to_large_remains(obj_clicks)
        obj_clicks = take_uncharged_cells(obj_clicks)
        obj_clicks = mine_large_remains(obj_clicks)
        obj_clicks = leave_large_remains_area(obj_clicks)
        obj_clicks = frag_port_available(obj_clicks)
        obj_clicks = mine_huge_remains(obj_clicks)
        obj_clicks = leave_huge_remains(obj_clicks)
        obj_clicks = make_essencev2(obj_clicks)
        npc_clicks = charge_guardian(npc_clicks)
        obj_clicks = enter_active_rift(obj_clicks)
        obj_clicks = make_airs(obj_clicks)
        obj_clicks = leave_air_altar(obj_clicks)
        obj_clicks = make_fires(obj_clicks)
        obj_clicks = leave_fire_altar(obj_clicks)
        obj_clicks = make_earths(obj_clicks)
        obj_clicks = leave_earth_altar(obj_clicks)
        obj_clicks = make_waters(obj_clicks)
        obj_clicks = leave_water_altar(obj_clicks)
# anim id 9365 whole time at carfting table fro ess
# refactor the make ess function based on this
# getting trapped in areas, need to make a click time out
# also need to deposit runes before i make more ess to free inv slots
main()
# overpowered orb - 26886
# strong orb - 26878
# med orb - 26884
# weak cell - 26883
