import datetime
import osrs

script_config = {
    'intensity': 'low',
    'logout': False,
    'login': False
}

frag_portal_dict = {
    'S': {'x': 3615, 'y': 9490, 'z': 0},
    'E': {'x': 3628, 'y': 9499, 'z': 0},
    'SE': {'x': 3623, 'y': 9495, 'z': 0},
    'SW': {'x': 3607, 'y': 9492, 'z': 0}
}

sprite_to_rift_obj_dict = {
    '4353': {  # air
        'tile': '3617,9494,0',
        'id': '43701',
        'tile_obj': {
            'x': 3617,
            'y': 9494,
            'z': 0
        }
    },
    '4359': {  # cosmic
        'tile': '3621,9496,0',
        'id': '43710',
        'tile_obj': {
            'x': 3621,
            'y': 9496,
            'z': 0
        }
    },
    '4355': {  # water
        'tile': '3623,9500,0',
        'id': '43702',
        'tile_obj': {
            'x': 3623,
            'y': 9500,
            'z': 0
        }
    },
    '4356': {  # earth
        'tile': '3623,9505,0',
        'id': '43703',
        'tile_obj': {
            'x': 3623,
            'y': 9505,
            'z': 0
        }
    },
    '4361': {  # nat
        'tile': '3621,9509,0',
        'id': '43711',
        'tile_obj': {
            'x': 3621,
            'y': 9509,
            'z': 0
        }
    },
    '4357': {  # fire
        'tile': '3617,9511,0',
        'id': '43704',
        'tile_obj': {
            'x': 3617,
            'y': 9511,
            'z': 0
        }
    },
    '4364': {  # blood
        'tile': '3612,9511,0',
        'id': '43708',
        'tile_obj': {
            'x': 3612,
            'y': 9511,
            'z': 0
        }
    },
    '4362': {  # law
        'tile': '3609,9510,0',
        'id': '43712',
        'tile_obj': {
            'x': 3609,
            'y': 9510,
            'z': 0
        }
    },
    '4363': {  # death
        'tile': '3607,9506,0',
        'id': '43707',
        'tile_obj': {
            'x': 3607,
            'y': 9506,
            'z': 0
        }
    },
    '4360': {  # chaos
        'tile': '3607,9501,0',
        'id': '43706',
        'tile_obj': {
            'x': 3607,
            'y': 9501,
            'z': 0
        }
    },
    '4358': {  # body
        'tile': '3609,9497,0',
        'id': '43709',
        'tile_obj': {
            'x': 3609,
            'y': 9497,
            'z': 0
        }
    },
    '4354': {  # mind
        'tile': '3612,9495,0',
        'id': '43705',
        'tile_obj': {
            'x': 3612,
            'y': 9495,
            'z': 0
        }
    }
}


available_catalytic_altars = [
    '4354',  # mind
    '4358',  # body
    '4360',  # chaos
    '4361',  # nature
]


def game_active(widgets):
    return bool(widgets) and '746,23' in widgets


def is_pregame(widgets):
    beginning = widgets and '746,23' in widgets and widgets['746,23']
    if beginning and 'spriteID' in beginning and beginning['spriteID'] == 4369:
        return True
    return False


def in_main_arena(loc):
    if loc and 'x' in loc and 3597 <= loc['x'] <= 3633 and 'y' in loc and 9484 <= loc['y'] <= 9519:
        return True
    else:
        return False


#use when logging back in
def outside_main_arena(loc):
    if loc and 'x' in loc and 3609 <= loc['x'] <= 3620 and 'y' in loc and loc['y'] <= 9483:
        return True
    else:
        return False


def click_allowed(last_click, target, timeout):
    if target in last_click and (datetime.datetime.now() - last_click[target]).total_seconds() < timeout:
        return False
    else:
        return True


def run_to_large_remains(status_obj, qh):
    inv = osrs.inv.get_inv()
    uncharged_cell = osrs.inv.is_item_in_inventory_v2(inv, 26882)
    if (not game_active(qh.get_widgets()) or is_pregame(qh.get_widgets())) \
            and in_main_arena(qh.get_player_world_location()) \
            and click_allowed(status_obj, '43724', 10) and uncharged_cell and uncharged_cell['quantity'] == 10:
        print('in run to large remains')
        obstacle = osrs.server.get_ground_object('3634,9503,0', '43724')
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            return {'43724': datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2({'x': 3626, 'y': 9500, 'z': 0})
    return status_obj


def mine_large_remains(status_obj, qh):
    loc = qh.get_player_world_location()
    inv = qh.get_inventory()
    guardian_frags = osrs.inv.is_item_in_inventory_v2(inv, 26878)
    if 'x' in loc and loc['x'] >= 3637 and \
            (not guardian_frags or guardian_frags and guardian_frags['quantity'] < 150) \
            and not qh.get_is_mining() and game_active(qh.get_widgets()) and click_allowed(status_obj, '43719', 5):
        print('in mine large remains')
        rock = osrs.server.get_game_object('3640,9498,0', '43719')
        if rock:
            osrs.move.move_and_click(rock['x'], rock['y'], 3, 3)
            return {'43719': datetime.datetime.now()}
    return status_obj


def leave_large_remains_area(status_obj, qh):
    loc = qh.get_player_world_location()
    inv = qh.get_inventory()
    guardian_frags = osrs.inv.is_item_in_inventory_v2(inv, 26878)
    if 'x' in loc and loc['x'] >= 3637 and \
            guardian_frags and guardian_frags['quantity'] > 150 \
            and not is_pregame(qh.get_widgets()) \
            and click_allowed(status_obj, '43726', 5):
        print('in leave large remains')
        obstacle = osrs.server.get_ground_object('3636,9503,0', '43726')
        if obstacle:
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.sleep_one_tick()
            return {'43726': datetime.datetime.now()}
    return status_obj


def take_uncharged_cells(status_obj, qh):
    inv = qh.get_inventory()
    uncharged_cell = osrs.inv.is_item_in_inventory_v2(inv, 26882)
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    if in_main_arena(qh.get_player_world_location()) \
            and (not game_active(qh.get_widgets()) or is_pregame(qh.get_widgets())) \
            and (not uncharged_cell or uncharged_cell and uncharged_cell['quantity'] < 10) \
            and not (elem_guardian_stone or catalytic_guardian_stone) \
            and click_allowed(status_obj, '43732', 5):
        print('in take uncharged cells')
        table = osrs.server.get_game_object('3618,9488,0', '43732')
        # if i am far north of the cell table, when i right click the menu opens above the cursor and i cant get a cell
        if table and 'dist' in table and table['dist'] < 7:
            osrs.move.right_click_menu_select(table, None, '56799', 'Uncharged cells', 'Take-10')
            return {'43732': datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2({'x': 3618, 'y': 9488, 'z': 0})
    return status_obj


def open_portal(widgets):
    portal_text = widgets and '746,28' in widgets and widgets['746,28']
    if portal_text \
            and 'text' in portal_text \
            and bool(portal_text['text']):
        text_parts = portal_text['text'].split(' - ')
        if len(text_parts) >= 2 and text_parts[1] != '0:00':
            return text_parts[0]
    else:
        return False


def frag_port_available(status_obj, qh):
    portal_text = open_portal(qh.get_widgets())
    inv = qh.get_inventory()
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    powered_cells = osrs.inv.are_items_in_inventory_v2(
        inv,
        [
            26885,  # strong
            26884,  # medium
            26886  # overpowered
        ]
    )
    if portal_text \
            and in_main_arena(qh.get_player_world_location()) \
            and len(inv) < 19 \
            and not powered_cells \
            and not (elem_guardian_stone or catalytic_guardian_stone) \
            and click_allowed(status_obj, '43729', 5):
        print('in frag port available')
        orb = osrs.server.get_surrounding_game_objects(10, ['43729'])
        if orb and '43729' in orb:
            osrs.move.move_and_click(orb['43729']['x'], orb['43729']['y'], 1, 1)
            return {'43729': datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2(frag_portal_dict[portal_text])

    return status_obj


# need to make this more precise with coords
def mine_huge_remains(status_obj, qh):
    loc = qh.get_player_world_location()
    inv = qh.get_inventory()
    if loc \
            and 'x' in loc \
            and 3594 >= loc['x'] >= 3586 \
            and len(inv) < 28 \
            and not osrs.server.is_mining() \
            and click_allowed(status_obj, '43720', 5) \
            and game_active(qh.get_widgets()):
        print('in mine huge remains')
        remains = osrs.server.get_surrounding_game_objects(8, ['43720'])
        if remains and '43720' in remains:
            osrs.move.move_and_click(remains['43720']['x'], remains['43720']['y'], 3, 3)
            return {'43720': datetime.datetime.now()}
    return status_obj


def leave_huge_remains(status_obj, qh):
    loc = qh.get_player_world_location()
    inv = qh.get_inventory()
    if loc \
            and 'x' in loc \
            and 3594 >= loc['x'] >= 3585 \
            and (len(inv) == 28 or not game_active(qh.get_widgets())) \
            and click_allowed(status_obj, '38044', 5):
        print('in leave huge remains')
        remains = osrs.server.get_game_object('3593,9503,0', '38044')
        if remains:
            osrs.move.move_and_click(remains['x'], remains['y'], 3, 3)
            return {'38044': datetime.datetime.now()}
    return status_obj


def make_essence_v2(status_obj, qh):
    inv = qh.get_inventory()
    guardian_frags = osrs.inv.is_item_in_inventory_v2(inv, 26878)
    guardian_ess = osrs.inv.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    portal_text = open_portal(qh.get_widgets())
    powered_cells = osrs.inv.are_items_in_inventory_v2(
        inv,
        [
            26885,  # strong
            26884,  # medium
            26886  # overpowered
        ]
    )
    if in_main_arena(qh.get_player_world_location()) \
            and guardian_frags \
            and guardian_frags['quantity'] > 24 \
            and (not guardian_ess or len(inv) < 28) \
            and not (elem_guardian_stone or catalytic_guardian_stone) \
            and qh.get_player_animation() != 9365 \
            and not portal_text \
            and not powered_cells:
        if osrs.inv.are_items_in_inventory_v2(inv, [554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565]):
            print('have runes')
            rune_deposit = osrs.server.get_game_object('3609,9487,0', '43696')
            if rune_deposit:
                if click_allowed(status_obj, '43696', 5):
                    print('found depo')
                    osrs.move.move_and_click(rune_deposit['x'], rune_deposit['y'], 3, 3)
                    return {'43696': datetime.datetime.now()}
            else:
                osrs.move.run_towards_square_v2({'x': 3609, 'y': 9487, 'z': 0})
        else:
            workbench = osrs.server.get_game_object('3612,9487,0', '43754')
            if workbench:
                if click_allowed(status_obj, '43754', 5):
                    osrs.move.move_and_click(workbench['x'], workbench['y'], 3, 3)
                    return {'43754': datetime.datetime.now()}
            else:
                osrs.move.run_towards_square_v2({'x': 3612, 'y': 9487, 'z': 0})
    return status_obj


def in_air_altar(loc):
    if 'x' in loc and 2835 <= loc['x'] <= 2851:
        return True
    else:
        return False


def in_mind_altar(loc):
    if 'x' in loc and 2761 <= loc['x'] <= 2802:
        return True
    else:
        return False


def in_body_altar(loc):
    if 'x' in loc and 2506 <= loc['x'] <= 2538:
        return True
    else:
        return False


def in_chaos_altar(loc):
    if 'x' in loc and 2242 <= loc['x'] <= 2296:
        return True
    else:
        return False


def in_nature_altar(loc):
    if 'x' in loc and 2390 <= loc['x'] <= 2409 and 4832 <= loc['y'] <= 4851:
        return True
    else:
        return False


# catalytic energy text of 746,24 split on :
# elem energy 746,21
def determine_rift():
    data_points = osrs.server.get_widgets(['746,24', '746,21', '746,20', '746,23'])
    cata_points = data_points and '746,24' in data_points and 'text' in data_points['746,24'] and data_points['746,24'][
        'text']
    elem_points = data_points and '746,21' in data_points and 'text' in data_points['746,21'] and data_points['746,21'][
        'text']
    cata_rift = data_points and '746,23' in data_points and 'spriteID' in data_points['746,23'] and data_points['746,23'][
        'spriteID']
    elem_rift = data_points and '746,20' in data_points and 'spriteID' in data_points['746,20'] and data_points['746,20'][
        'spriteID']

    elem_points = isinstance(elem_points, str) and elem_points.split(' ')[1]
    cata_points = isinstance(cata_points, str) and cata_points.split(' ')[1]

    if int(cata_points) - int(elem_points) > 50 or not str(cata_rift) in available_catalytic_altars:
        return str(elem_rift) in sprite_to_rift_obj_dict and sprite_to_rift_obj_dict[str(elem_rift)]
    else:
        return str(cata_rift) in sprite_to_rift_obj_dict and sprite_to_rift_obj_dict[str(cata_rift)]


def enter_active_rift_v2(status_obj, qh):
    inv = qh.get_inventory()
    guardian_ess = osrs.inv.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    portal_text = open_portal(qh.get_widgets())
    guardian_frags = osrs.inv.is_item_in_inventory_v2(inv, 26878)
    if in_main_arena(qh.get_player_world_location()) \
            and ((guardian_ess and len(inv) == 28) or (guardian_ess and not guardian_frags)) \
            and qh.get_player_animation() != 9365 \
            and (not portal_text or (portal_text and len(inv) == 28)) \
            and not (elem_guardian_stone or catalytic_guardian_stone):
        rift_to_enter = determine_rift()
        if rift_to_enter and click_allowed(status_obj, rift_to_enter['id'], 5):
            print('rift to enter', rift_to_enter)
            rift = osrs.server.get_game_object(rift_to_enter['tile'], rift_to_enter['id'])
            if rift:
                osrs.move.move_and_click(rift['x'], rift['y'], 3, 4)
                return {rift_to_enter['id']: datetime.datetime.now()}
            else:
                osrs.move.run_towards_square_v2(rift_to_enter['tile_obj'])
    return status_obj


def in_fire_altar(loc):
    if 'x' in loc and 2560 <= loc['x'] <= 2605:
        return True
    else:
        return False


def in_earth_altar(loc):
    if 'x' in loc and 2628 <= loc['x'] <= 2680:
        return True
    else:
        return False


def in_water_altar(loc):
    if 'x' in loc and 2707 <= loc['x'] <= 2732:
        return True
    else:
        return False


def leave_altar(status_obj, location_function, tile, exit_id, qh, rune):
    inv = qh.get_inventory()
    guardian_ess = osrs.inv.is_item_in_inventory_v2(inv, 26879)
    if location_function(qh.get_player_world_location()) and not guardian_ess and click_allowed(status_obj, exit_id, 8):
        print('leaving {} altar'.format(rune))
        exit_obj = osrs.server.get_game_object('{},{},{}'.format(tile['x'], tile['y'], tile['z']), exit_id)
        if exit_obj:
            osrs.move.move_and_click(exit_obj['x'], exit_obj['y'], 3, 3)
            return {exit_id: datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2(tile)
    return status_obj


def craft_rune(status_obj, location_function, tile, altar_id, qh, rune):
    inv = qh.get_inventory()
    guardian_ess = osrs.inv.is_item_in_inventory_v2(inv, 26879)
    if location_function(qh.get_player_world_location()) and guardian_ess and click_allowed(status_obj, altar_id, 5):
        print('craft {} runes'.format(rune))
        altar = osrs.server.get_game_object('{},{},{}'.format(tile['x'], tile['y'], tile['z']), altar_id)
        if altar:
            osrs.move.move_and_click(altar['x'], altar['y'], 3, 3)
            return {altar_id: datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2(tile)
    return status_obj


def charge_guardian(status_obj, qh):
    inv = qh.get_inventory()
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    if in_main_arena(qh.get_player_world_location()) \
            and (elem_guardian_stone or catalytic_guardian_stone) \
            and click_allowed(status_obj, '11403', 5):
        print('charging guardian')
        guardian = osrs.server.get_npcs_by_id('11403')
        if len(guardian) > 0:
            osrs.move.move_and_click(guardian[0]['x'], guardian[0]['y'], 3, 3)
            return {'11403': datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2({'x': 3615, 'y': 9503, 'z': 0})
    return status_obj


def place_charged_cells(status_obj, qh):
    inv = qh.get_inventory()
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    powered_cells = osrs.inv.are_items_in_inventory_v2(
        inv,
        [
            26885,  # strong
            26884,  # medium
            26886  # overpowered
        ]
    )
    if in_main_arena(qh.get_player_world_location()) \
            and powered_cells \
            and click_allowed(status_obj, '3608,9503,0', 5) \
            and not (elem_guardian_stone or catalytic_guardian_stone) \
            and game_active(qh.get_widgets()):
        print('placing charged cell')
        osrs.move.spam_click('3608,9503,0', 1.5)
        return {'3608,9503,0': datetime.datetime.now()}
    return status_obj


# currently if i have less than 24 guardian frags in bag it doesnt do anything
def mine_regular_guardian_remains(status_obj, qh):
    inv = qh.get_inventory()
    guardian_frags = osrs.inv.is_item_in_inventory_v2(inv, 26878)
    guardian_ess = osrs.inv.is_item_in_inventory_v2(inv, 26879)
    elem_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26881)
    catalytic_guardian_stone = osrs.inv.is_item_in_inventory_v2(inv, 26880)
    portal_text = open_portal(qh.get_widgets())
    powered_cells = osrs.inv.are_items_in_inventory_v2(
        inv,
        [
            26885,  # strong
            26884,  # medium
            26886  # overpowered
        ]
    )
    if in_main_arena(qh.get_player_world_location()) \
            and game_active(qh.get_widgets()) \
            and (not guardian_frags or (guardian_frags and guardian_frags['quantity'] <= 24)) \
            and not guardian_ess \
            and not qh.get_is_mining() \
            and not powered_cells \
            and not portal_text \
            and not elem_guardian_stone \
            and not catalytic_guardian_stone \
            and click_allowed(status_obj, '43717', 5) \
            and not is_pregame(qh.get_widgets()):
        remains = osrs.server.get_game_object('3602,9491,0', '43717')
        if remains:
            osrs.move.move_and_click(remains['x'], remains['y'], 3, 3)
            return {'43717': datetime.datetime.now()}
        else:
            osrs.move.run_towards_square_v2({'x': 3606, 'y': 9491, 'z': 0})
    return status_obj


def enter_arena(status_obj, qh):
    if outside_main_arena(qh.get_player_world_location()) and click_allowed(status_obj, '43700', 2):
        remains = osrs.server.get_game_object('3615,9483,0', '43700')
        if remains:
            osrs.move.move_and_click(remains['x'], remains['y'], 3, 3)
            return {'43700': datetime.datetime.now()}
        elif click_allowed(status_obj, '000', 30):
            loc = osrs.server.get_world_location()
            if loc:
                osrs.move.spam_click('3617,9482,0', 1)
                return {'000': datetime.datetime.now()}
    return status_obj


def turn_on_run(widgets):
    run_orb = widgets and '160,29' in widgets and widgets['160,29']
    if run_orb:
        if run_orb['spriteID'] != 1065:
            osrs.move.fast_move_and_click(run_orb['x'], run_orb['y'], 3, 3)
        return


def check_for_logout(qh):
    if in_main_arena(qh.get_player_world_location()) \
            and (not game_active(qh.get_widgets()) or is_pregame(qh.get_widgets())):
        osrs.game.break_manager_v3(script_config)

def main():
    clicks = {}
    qh = osrs.queryHelper.QueryHelper()
    while True:
        qh.inventory()
        qh.player_world_location()
        qh.is_mining()
        qh.player_animation()
        qh.widgets(['746,23', '746,28', '160,29'])
        qh.query_backend()
        turn_on_run(qh.get_widgets())
        clicks = enter_arena(clicks, qh)
        clicks = take_uncharged_cells(clicks, qh)
        clicks = run_to_large_remains(clicks, qh)
        clicks = mine_large_remains(clicks, qh)
        clicks = leave_large_remains_area(clicks, qh)
        clicks = frag_port_available(clicks, qh)
        clicks = mine_huge_remains(clicks, qh)
        clicks = leave_huge_remains(clicks, qh)
        clicks = enter_active_rift_v2(clicks, qh)
        clicks = craft_rune(clicks, in_air_altar, {'x': 2844, 'y': 4834, 'z': 0}, '34760', qh, 'air')
        clicks = craft_rune(clicks, in_fire_altar, {'x': 2585, 'y': 4839, 'z': 0}, '34764', qh, 'fire')
        clicks = craft_rune(clicks, in_earth_altar, {'x': 2658, 'y': 4841, 'z': 0}, '34763', qh, 'earth')
        clicks = craft_rune(clicks, in_water_altar, {'x': 2716, 'y': 4836, 'z': 0}, '34762', qh, 'water')
        clicks = craft_rune(clicks, in_mind_altar, {'x': 2787, 'y': 4840, 'z': 0}, '34761', qh, 'mind')
        clicks = craft_rune(clicks, in_body_altar, {'x': 2523, 'y': 4840, 'z': 0}, '34765', qh, 'body')
        clicks = craft_rune(clicks, in_chaos_altar, {'x': 2271, 'y': 4842, 'z': 0}, '34769', qh, 'chaos')
        clicks = craft_rune(clicks, in_nature_altar, {'x': 2400, 'y': 4841, 'z': 0}, '34768', qh, 'nature')
        clicks = leave_altar(clicks, in_air_altar, {'x': 2841, 'y': 4828, 'z': 0}, '34748', qh, 'air')
        clicks = leave_altar(clicks, in_fire_altar, {'x': 2574, 'y': 4850, 'z': 0}, '34752', qh, 'fire')
        clicks = leave_altar(clicks, in_earth_altar, {'x': 2655, 'y': 4829, 'z': 0}, '34751', qh, 'earth')
        clicks = leave_altar(clicks, in_water_altar, {'x': 2727, 'y': 4832, 'z': 0}, '34750', qh, 'water')
        clicks = leave_altar(clicks, in_mind_altar, {'x': 2793, 'y': 4827, 'z': 0}, '34749', qh, 'mind')
        clicks = leave_altar(clicks, in_body_altar, {'x': 2521, 'y': 4833, 'z': 0}, '34753', qh, 'body')
        clicks = leave_altar(clicks, in_chaos_altar, {'x': 2282, 'y': 4837, 'z': 0}, '34757', qh, 'chaos')
        clicks = leave_altar(clicks, in_nature_altar, {'x': 2400, 'y': 4834, 'z': 0}, '34756', qh, 'nature')
        clicks = charge_guardian(clicks, qh)
        clicks = place_charged_cells(clicks, qh)
        clicks = make_essence_v2(clicks, qh)
        clicks = mine_regular_guardian_remains(clicks, qh)
        check_for_logout(qh)


# it wont craft nats, need to investigate
main()
